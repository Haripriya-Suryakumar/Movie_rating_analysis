from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import requests
import os

app = FastAPI()

# Cosmos DB connection
COSMOS_DB_CONNECTION_STRING = "your_cosmos_db_connection_string"
client = MongoClient(COSMOS_DB_CONNECTION_STRING)
db = client["movie_db"]
collection = db["movies"]

# OMDB API Key
OMDB_API_KEY = "b7cf78a3"

@app.get("/")
def home():
    return {"message": "Movie API is running"}

@app.get("/movie/{movie_name}")
def get_movie(movie_name: str):
    # Check if movie exists in the database
    movie_data = collection.find_one({"title": movie_name}, {"_id": 0})
    if movie_data:
        return movie_data

    # Fetch from OMDB API
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "False":
        raise HTTPException(status_code=404, detail="Movie not found")

    # Store in database
    collection.insert_one(data)

    return data
