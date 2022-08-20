from fastapi import FastAPI,Path
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from data_model import *

from typing import Union
from pydantic import BaseModel
import pymongo
import json

DB_CLIENT_ADDRESS="mongodb://localhost:27017/"



app = FastAPI()

origins = [
 
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,

    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message":"Hello world"}

@app.post("/dht22/{userid}")

async def receive_temperature(
    data: DHT22,
   
    userid:str=Path(...,title='user id',description="The id of user") 
    ):
    '''
    Receive the dht22 data from smart station and write the data into the corresponding data base.
    '''

    client = pymongo.MongoClient(DB_CLIENT_ADDRESS)
    dht_db = client['dht22']
    
    dht_table = dht_db[userid]
    dht_table.insert_one(jsonable_encoder(data))
    
    return data

@app.get("/dht22/{userid}/")
async def query_last(
    userid:str=Path(...,title='user id',description="The id of user") 
):
    '''
    Get the lastest one recording of the data base.

    Return:
        last_record: a recording in dict() type
    
    '''
    client = pymongo.MongoClient(DB_CLIENT_ADDRESS)
    dht_db = client["dht22"]
    dht_table = dht_db[userid]
    last_record = dht_table.find_one(sort=[( '_id', pymongo.DESCENDING )])
    last_record.pop('_id')

    return last_record
