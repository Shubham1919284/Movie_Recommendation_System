# 🎬 Dynamic Movie Recommendation System

A real-time movie recommender built using Python, Flask, and TMDB API. Suggests movies dynamically based on input title using content metadata like genres, cast, overview, and recent releases — without relying on any static similarity file.

## 🔍 Features

- Dynamic movie search via TMDB API
- Recommends similar movies based on genres, cast, and release year
- Prioritizes sequels and newer releases
- No local similarity matrix or dataset needed
- Clean, responsive front-end using Flask + HTML/CSS

## 🚀 Tech Stack

- Python
- Flask
- TMDB API
- HTML/CSS
- Jinja2 templating

## 🧠 How it Works

1. User inputs a movie title in the web UI.
2. App queries TMDB API in real time to fetch movie metadata.
3. Matches are based on:
   - Movie series (franchise/sequels if found)
   - Similar genres and cast
   - Release year proximity (e.g., ±2 years)
4. Top 5 similar or relevant movies are shown with poster images.

## 📂 Project Structure

├── app.py               # Main Flask backend logic
├── templates/
│   └── index.html       # UI with input & output sections

## 📥 How to Run

# 1. Clone the repository
git clone https://github.com/Shubham1919284/Dynamic-Movie-Recommendation-System.git
cd Dynamic-Movie-Recommendation-System

# 2. Install required packages
pip install flask requests httpx

# 3. Add your TMDB API key
# (Open app.py and replace TMDB_API_KEY with your key)

# 4. Run the Flask app
python app.py

# 5. Open the app in your browser
http://127.0.0.1:5000


## 📝 Notes

- Requires a valid TMDB API key (set inside `app.py`)
- Works only with valid movie titles recognized by TMDB
- Internet connection required (relies on API calls)

## 👨‍💻 Author

**Shubham Kumar Jha**  
BTech CSE (Data Science), Gulzar Group of Institutes (PTU)  
📧 sk1919284@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/shubham-kumar-jha-1a2b3c)  
💻 [GitHub](https://github.com/Shubham1919284)

## 🏷️ Topics
`TMDB API` `Flask` `Python` `Movie Recommendation` `Dynamic System` `Content-Based Filtering` `BTech Project` `Student Portfolio`
