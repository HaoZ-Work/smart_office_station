import os
import urequests as requests
import network
import time
import dht
import machine
import json

from machine import Pin, SoftI2C,SPI
import ssd1306

Base_URL = 'http://103.124.104.160:8000/'

# class sensor_dht22():
#   def __init__(self):
#     pass
  
#   def sent_data():
    



def main():
 
  # ESP32 Pin assignment 
  i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

  oled_width = 128
  oled_height = 64
  oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
  oled.text("Connecting...",0,0)

  print("Connecting to WiFi", end="")
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  # sta_if.connect('Wokwi-GUEST', '')
  sta_if.connect('H2G', 'zh970201')
  while not sta_if.isconnected():
    print(".", end="")
    time.sleep(1)
  print("Connected!")
  oled.text("WiFi Connected!!",0,10)
  oled.show()
  time.sleep(0.5)
  



  d = dht.DHT22(machine.Pin(14))
  # d.measure()
  data = dict()
  data['name']='dht'
  while True:
    oled.fill(0)
    d.measure()
    # print(d.temperature())
    data['temperature']=d.temperature()
    data['humidity'] = d.humidity()
    oled.text(f"WiFi connected.",0,0)
    oled.text(f"temperatrue:{d.temperature()}",0,10)
    
    oled.text(f"humidity:{d.humidity()}",0,20)
    
    oled.show()
   
    # oled.text(d.humidity(),0,30)




    res = requests.post(
    url=Base_URL+'dht22/user01',
    data = json.dumps(data)
    )
    print(res.json())
    time.sleep(0.1)

  


 
if __name__ == '__main__':
  main()
