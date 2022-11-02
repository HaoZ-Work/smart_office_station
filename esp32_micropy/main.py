import os
import urequests as requests
import network
import time
import dht
import machine
import ujson
import socket

from machine import Pin, SoftI2C,SPI
import ssd1306

CONFIG_PATH = './config.json'
WIFI_SETUP_TEMPLATE = './WiFi_setup.html'


class SmartOfficeStation():
  def __init__(self) -> None:
     self._oled_init()
     self._wifi_connect()

  
  def _save_SSID(self,ssid,passwd):
    '''
    Save SSID name and password to config.json file.

    '''

    with open(CONFIG_PATH,"w") as dump_file:
      ssid_config={
        "SSID":ssid,
        "SSID_PASS":passwd
      }
       
      ujson.dump(ssid_config,dump_file)
    

  def _get_SSID(self):
    '''
    Import the SSID name and password from config.json file.
    
    '''
    with open(CONFIG_PATH,"r") as config_file:
      config = ujson.load(config_file)
      # print(config)

    ssid = config['SSID']
    passwd = config['SSID_PASS']
    
    return ssid,passwd
    

  def _wifi_setup(self):
    '''
    If the default SSID and password can not make device connect to internet, then enable AP mode and hold a website on port 80 of the device. 
    User can type SSID name and password in the website. Ths SSID and password will be saved into local file and returned.

    Return:
      ssid,password: User typed ssid and password
    
    '''
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='ESP32')
    self.webserver()

    self._save_SSID("H2G","zh970201")
    ssid,passwd = self._get_SSID()
    return ssid,passwd
  
  def _wifi_connect(self):

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    sta_if.config(reconnects=-1)
    self.oled.text("Connecting...",0,0)
    
    print('connecting to network...')
    sta_if.disconnect()
    SSID,SSID_PASS=self._get_SSID()
    sta_if.connect(SSID,SSID_PASS)
    time.sleep(5)

    if not sta_if.isconnected():

      self.oled.text("Enable Ap model",0,10)
          
      print("Enable Ap model")
          
      sta_if.active(True)

      new_SSID,new_SSID_PASS=self._wifi_setup()
      sta_if.disconnect()
      sta_if.connect(new_SSID,new_SSID_PASS)
    
    while sta_if.isconnected()!=True:
      print("Connecting...")
      print(sta_if.isconnected())
    print('network config:', sta_if.ifconfig())
    self.oled.text("WiFi connected.",0,20)
    self.oled.text(f"{sta_if.ifconfig()[0]}",0,30)
    self.oled.show()

  def webserver(self):
    # html = """<!DOCTYPE html>
    # <html>
    #     <head> <title>ESP8266 Pins</title> </head>
    #     <body> <h1>ESP8266 Pins</h1>
    #         <p>Hello!</p>
    #     </body>
    # </html>
    # """
    with open(WIFI_SETUP_TEMPLATE,'r') as f:
      html = f.read()
    print(html)
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    # 192.168.1.1:80
    # 192.168.1.1:80/setup_wifi.html
    
    s = socket.socket()
    
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)
    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        
        response = html 
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
  
  def _oled_init(self):
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    self.oled = oled
    # oled.text("Connecting...",0,0)
    # oled.show()




def main():

   smartoffice = SmartOfficeStation()
  #  smartoffice.webserver()
  

if __name__ == '__main__':
  main()
