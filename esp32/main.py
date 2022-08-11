import os
import urequests as requests
import network
import time
import dht
import machine
import json
Base_URL = 'http://103.124.104.160:8000/'


    



def main():
  print("Connecting to WiFi", end="")
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  sta_if.connect('Wokwi-GUEST', '')
  while not sta_if.isconnected():
    print(".", end="")
    time.sleep(1)
  print(" Connected!")



  d = dht.DHT22(machine.Pin(23))
  # d.measure()
  data = dict()
  data['name']='dht'
  while True:
    d.measure()
    data['temperature']=d.temperature()
    data['humidity'] = d.humidity()



    res = requests.post(
    url=Base_URL+'dht22_data/',
    data = json.dumps(data)
    )
    print(res.json())
    time.sleep(0.1)

  


 
if __name__ == '__main__':
  main()
