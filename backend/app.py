from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
OMDB_API_KEY = os.getenv("OMDB_API_KEY") 

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['GET'])
def search_movie():
    query = request.args.get('query')
    if not query:
        return render_template("index.html")

    # Fetch movie data from OMDB API
    url = f"http://www.omdbapi.com/?t={query}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        rating_str = response.get('imdbRating', '0')
        try:
            rating = min(float(rating_str) / 2, 5.0)  
        except (ValueError, TypeError):
            rating = 0
        
        full_stars = int(rating)
        half_star = 1 if (rating - full_stars) >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star

        # Prepare movie data
        movie = {
            'Title': response.get('Title'),
            'Year': response.get('Year'),
            'Genre': response.get('Genre'),
            'Director': response.get('Director'),
            'Actors': response.get('Actors'),
            'Plot': response.get('Plot'),
            'Poster': response.get('Poster'),
            'imdbRating': rating_str,
            'full_stars': full_stars,
            'half_star': half_star,
            'empty_stars': empty_stars
        }
    else:
        movie = None

    # Render the results template with movie data
    return render_template("results.html", movie=movie)

if __name__ == '__main__':
    app.run(debug=True)