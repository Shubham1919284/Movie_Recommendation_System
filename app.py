from flask import Flask, render_template, request
import requests
from urllib.parse import quote

app = Flask(__name__)

# Your TMDB API Key
tmdb_api_key = "Your_API_Key"

def fetch_movie_data_from_api(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={quote(movie_title)}"
    response = requests.get(url).json()
    if response['results']:
        best_match = sorted(response['results'], key=lambda x: x.get('popularity', 0), reverse=True)[0]
        movie_id = best_match['id']
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&append_to_response=similar,credits"
        details = requests.get(details_url).json()
        return {
            "title": details.get("title"),
            "genre": [g["name"] for g in details.get("genres", [])],
            "year": details.get("release_date", "")[:4],
            "cast": [c["name"] for c in details.get("credits", {}).get("cast", [])[:5]],
            "director": [c["name"] for c in details.get("credits", {}).get("crew", []) if c["job"] == "Director"],
            "similar": details.get("similar", {}).get("results", [])
        }, best_match['id']
    return None, None

def fetch_movie_collection(movie_id):
    collection_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}"
    try:
        resp = requests.get(collection_url, timeout=5)
        resp.raise_for_status()
        details = resp.json()
    except Exception as e:
        print(f"Error fetching collection for movie_id {movie_id}: {e}")
        return [], None

    if not details or not isinstance(details, dict):
        return [], None

    collection = details.get("belongs_to_collection")
    collection_id = collection.get("id") if collection else None
    if collection_id:
        coll_url = f"https://api.themoviedb.org/3/collection/{collection_id}?api_key={tmdb_api_key}"
        try:
            coll = requests.get(coll_url, timeout=5).json()
        except Exception as e:
            print(f"Error fetching collection details for collection_id {collection_id}: {e}")
            return [], collection_id
        return [item['title'] for item in coll.get("parts", []) if 'release_date' in item and item['release_date'][:4].isdigit()], collection_id
    return [], None

def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={quote(movie_title)}"
    response = requests.get(url).json()
    if response['results'] and response['results'][0].get('poster_path'):
        return f"https://image.tmdb.org/t/p/w500{response['results'][0]['poster_path']}"
    return "https://via.placeholder.com/300x450?text=No+Poster"

def recommend(movie_title):
    movie_info, movie_id = fetch_movie_data_from_api(movie_title)
    if not movie_info:
        return [("Movie not found", "https://via.placeholder.com/300x450?text=Not+Found")], movie_title.title()

    recommendations = []
    used_titles = set()

def recommend(movie_title):
    movie_info, movie_id = fetch_movie_data_from_api(movie_title)
    if not movie_info:
        return [("Movie not found", "https://via.placeholder.com/300x450?text=Not+Found")], movie_title.title()

    recommendations = []
    used_titles = set()

    original_genres = set(movie_info.get("genre", []))
    original_year = int(movie_info.get("year", "2000"))

    # 1: Sequel or same collection
    sequels, collection_id = fetch_movie_collection(movie_id)
    for title in sequels:
        if title.lower() != movie_info['title'].lower():
            poster = fetch_poster(title)
            recommendations.append((title, poster))
            used_titles.add(title)
        if len(recommendations) >= 5:
            break

    # 2: Similar movies from TMDB similar API
    if len(recommendations) < 5:
        sorted_similars = sorted(
            movie_info['similar'],
            key=lambda x: x.get("release_date", "1900"),
            reverse=True
        )

        for movie in sorted_similars:
            title = movie.get("title")
            release_date = movie.get("release_date")
            if not title or not release_date or title in used_titles:
                continue

            year = int(release_date[:4])
            if year < original_year - 2:
                continue  # too old

            # Fetch genre 
            genre_url = f"https://api.themoviedb.org/3/movie/{movie['id']}?api_key={tmdb_api_key}"
            genre_resp = requests.get(genre_url).json()
            movie_genres = set([g['name'] for g in genre_resp.get('genres', [])])

            if not original_genres & movie_genres:
                continue  # no genre match

            poster = fetch_poster(title)
            recommendations.append((title, poster))
            used_titles.add(title)

            if len(recommendations) >= 5:
                break

    # 3: Fallback - Fill remaining with genre-matching popular recent movies
    if len(recommendations) < 5:
        genre_map_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={tmdb_api_key}&language=en-US"
        genre_data = requests.get(genre_map_url).json()
        genre_ids = []
        for g in original_genres:
            for g_map in genre_data.get('genres', []):
                if g_map['name'].lower() == g.lower():
                    genre_ids.append(str(g_map['id']))
        if genre_ids:
            fallback_url = (
                f"https://api.themoviedb.org/3/discover/movie?api_key={tmdb_api_key}"
                f"&sort_by=popularity.desc&with_genres={','.join(genre_ids)}"
                f"&primary_release_date.gte={original_year}&language=en-US&page=1"
            )
            fallback_resp = requests.get(fallback_url).json()
            for movie in fallback_resp.get("results", []):
                title = movie.get("title")
                if title and title not in used_titles:
                    poster = fetch_poster(title)
                    recommendations.append((title, poster))
                    used_titles.add(title)
                if len(recommendations) >= 5:
                    break

    return recommendations, movie_info['title']

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    movie_name = None
    if request.method == 'POST':
        movie_name = request.form['movie']
        recommendations, movie_name = recommend(movie_name)
    return render_template('index.html', recommendations=recommendations, movie_name=movie_name)

if __name__ == '__main__':
    app.run(debug=True)
