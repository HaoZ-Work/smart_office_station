from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from typing import Union
from pydantic import BaseModel
import pymongo
import json

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
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    dht_db = client["dht22"]
    dht_table = dht_db['station01']
    dht_table.insert_one(jsonable_encoder(item))
    
    return item
