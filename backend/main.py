from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from typing import Union
from pydantic import BaseModel
import pymongo
import json

DB_CLIENT_ADDRESS="mongodb://localhost:27017/"


class Item(BaseModel):
    name:str
    temperature:float
    humidity:float

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Hello world"}

@app.post("/dht22_data/")
async def receive_temperature(item:Item):
    client = pymongo.MongoClient(DB_CLIENT_ADDRESS)
    dht_db = client["dht22"]
    dht_table = dht_db['station01']
    dht_table.insert_one(jsonable_encoder(item))
    
    return item

@app.get("/dht22_data/get_last/")
async def query_last():
    client = pymongo.MongoClient(DB_CLIENT_ADDRESS)
    dht_db = client["dht22"]
    dht_table = dht_db['station01']
    last_record = dht_table.find_one(sort=[( '_id', pymongo.DESCENDING )])
    last_record.pop('_id')

    return last_record
