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

from microdot import Microdot,Response
from microdot_utemplate import render_template,init_templates



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


    
    '''
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='ESP32')
    
    Response.default_content_type = 'text/html'
    app=Microdot()
    @app.route('/', methods=['GET', 'POST'])
    def AP_index(request):
        if request.method == 'GET':
            return render_template('WiFi_setup.html',test='666')
        elif request.method == 'POST':
            ssid = request.form.get('SSID')
            ps = request.form.get('Pass')
            print(ssid,ps)
            self._save_SSID(ssid,ps)
            app.shutdown()
            ap.active(False)

            # return f"SSID:{ssid},pass:{ps}, server is shuting down.."
    
    app.run(host='0.0.0.0',port=80)


    
  
  def _wifi_connect(self):
    '''
    Make the ESP32 connect to wifi net. If the SSID and password in local config.json file are not available.Then enable AP model to get SSID and pass for user side.

    
    '''

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    sta_if.config(reconnects=-1)
    self.oled.text("Connecting...",0,0)
    
    print('connecting to network...')
    sta_if.disconnect()
    
    SSID,SSID_PASS=self._get_SSID()
    print(f"The initial SSID:{SSID} and pass:{SSID_PASS}")
    sta_if.connect(SSID,SSID_PASS)
    time.sleep(3)

    if not sta_if.isconnected():

      self.oled.text("Enable Ap model",0,10)
          
      print("Enable Ap model")
          

      self._wifi_setup()

      sta_if.disconnect()
      new_SSID,new_SSID_PASS=self._get_SSID()
      print(f"The  new SSID:{new_SSID} and pass:{new_SSID_PASS}")

      sta_if.connect(new_SSID,new_SSID_PASS)
      time.sleep(3)

    
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
  

  def server(self):
    app=Microdot()

    @app.route('/', methods=['GET', 'POST'])
    def server_index(request):
        if request.method == 'GET':
            return render_template('index.html',sensor_data={'key':'value'})
       
    print("Running server..")
    app.run(host='0.0.0.0',port=80)

  def _oled_init(self):
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    self.oled = oled
    # oled.text("Connecting...",0,0)
    # oled.show()




def main():
  Response.default_content_type = 'text/html'


  smartoffice = SmartOfficeStation()
  #smartoffice.server()
  # sta_if = network.WLAN(network.STA_IF)
  # sta_if.active(True)

  # sta_if.config(reconnects=-1)

    
  # print('connecting to network...')
  # sta_if.disconnect()
  # SSID = 'H2G'
  # SSID_PASS='zh970201'
  # sta_if.connect(SSID,SSID_PASS)
  # time.sleep(5)

  # app=Microdot()
  # # @app.get('/')
  # # def index(request):
  # #   # return 'Hello, world!'

  # #   return render_template('WiFi_setup.html',test='666')
  
  # # @app.post('/post')
  # # def post(request):
  # #   # return 'Hello, world!'
  # #   ssid = request.form.get('SSID')
  # #   ps = request.form.get('Pass')
  # #   print(ssid,ps)

  # #   return f'{ssid,ps}'
  # @app.route('/', methods=['GET', 'POST'])
  # def index(request):
  #     if request.method == 'GET':
  #         return render_template('WiFi_setup.html',test='666')
  #     elif request.method == 'POST':
  #         ssid = request.form.get('SSID')
  #         ps = request.form.get('Pass')
  #         print(ssid,ps)
  #         app.shutdown()
  #         return f"SSID:{ssid},pass:{ps}, server is shuting down.."
  
  # app.run()
  # print('SSID done!')

if __name__ == '__main__':
  main()
