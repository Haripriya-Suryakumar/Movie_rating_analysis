import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OMDB_API_KEY')
API_URL = "http://www.omdbapi.com/?apikey=" + API_KEY

def get_movie_details(movie_name):
    response = requests.get(API_URL, params={"t": movie_name})
    data = response.json()

    if data.get("Response") == "True":
        return {
            "title": data.get("Title"),
            "year": data.get("Year"),
            "genre": data.get("Genre"),
            "director": data.get("Director"),
            "plot": data.get("Plot"),
            "poster": data.get("Poster"),
        }
    return None


