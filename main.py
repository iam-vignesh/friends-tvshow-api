import contextlib
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
import random



app = FastAPI()
client = MongoClient('mongodb://localhost:27017/')
db = client['friends_episodes']
collection = db['friends_episodes']


@app.get("/")
def get_info():
    end_points =  {
            "get all episodes from a season": "/api/v1/season_number/all",
            "get specific episode": "/api/v1/season_number/episode_number",
            "get a random episode": "/api/v1/random"
        }

    info = {
        "title": "friends tv show api",
        "usage": "returns episode titles from the show based on season and episode numbers",
        "endpoints": end_points
    }
    return info

@app.get("/api/v1/{season_number}/all")
def get_all_season_episodes(season_number: str):

    query = {"season": season_number }
    projection = {"_id": 0, "title": 1}
    result = list(collection.find(query, projection))
    if not result:
        raise HTTPException(status_code=400, detail="Unable to find any matching seasons. Check if season number exists")
    episode_titles = [episode["title"] for episode in result]
    return {"titles":episode_titles}

@app.get("/api/v1/{season_number}/{episode_number}")
def get_episodes(season_number: str, episode_number: str):

    query = {"season": season_number, "number": episode_number }
    projection = {"_id": 0, "title": 1}
    result = collection.find_one(query, projection)
    if not result:
        raise HTTPException(status_code=400, detail="Episode not found. Check if episode number exists")
    return {"title":result['title']}

@app.get("/api/v1/random")
def get_episodes():

    season_number=str(random.randint(0, 10))
    episode_number=str(random.randint(0, 25))

    query = {"season": season_number, "number": episode_number }
    projection = {"_id": 0, "title": 1}
    result = collection.find_one(query, projection)
    if not result:
        raise HTTPException(status_code=400, detail="Unexpected error occured. Try again")
    return {"tilte":result['title'], "episode_info":query}