import contextlib
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

app = FastAPI()
client = MongoClient('mongodb://localhost:27017/')
db = client['friends_episodes']
collection = db['friends_episodes']


@app.get("/{season_number}/all")
def get_all_season_episodes(season_number: str):

    query = {"season": season_number }
    projection = {"_id": 0, "title": 1}
    result = list(collection.find(query, projection))
    if not result:
        raise HTTPException(status_code=400, detail="Unable to find any matching seasons. Check if season number exists")
    episode_titles = [episode["title"] for episode in result]
    return episode_titles

@app.get("/{season_number}/{episode_number}")
def get_episodes(season_number: str, episode_number: str):

    query = {"season": season_number, "number": episode_number }
    projection = {"_id": 0, "title": 1}
    result = collection.find_one(query, projection)
    if not result:
        raise HTTPException(status_code=400, detail="Episode not found. Check if episode number exists")
    return result['title']


