from pydantic import Field
from pydantic import BaseModel
from enum import Enum 
from typing import Union

class SensorData(BaseModel):
    name:str
 




class DHT22(SensorData):
    temperature:float=Field(
        default=0.0,
        title="temperature",
        description="temperature data in ^C from dht22 sensor",
        ge=-40.0,
        le=80.0)
    humidity:float=Field(
        default=0.0,
        title="humidity",
        description="humidity data in percentage  from dht22 sensor",
        ge=0.0,
        le=100.0)

# class SensorName(SensorData, Enum):
#     dht22=DHT22

# SensorName = {'dht22':DHT22}