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

from microdot import Microdot, Response,send_file
import uasyncio as asyncio

from microdot_asyncio import Microdot as async_Microdot

from microdot_utemplate import render_template,init_templates


CONFIG_PATH = './config.json'
# WIFI_SETUP_TEMPLATE = './WiFi_setup.html'


class SmartOfficeStation():
  def __init__(self) -> None:
     self._load_config()
     self._oled_init()
     self._wifi_connect()
     self._dht_init()

  def _load_config(self):
    '''
    Load configuration from config.json.Check the config.json for more details.

    '''
    with open(CONFIG_PATH,"r") as config_file:
      self.config = ujson.load(config_file)
    print(self.config)
  
  def _save_SSID(self,ssid,passwd):
    '''
    Save SSID name and password to config.json file.

    '''

    with open(CONFIG_PATH,"w") as dump_file:
      self.config["SSID"] = ssid
      self.config["SSID_PASS"]=passwd

      ujson.dump(self.config,dump_file)
    

  def _get_SSID(self):
    '''
    Import the SSID name and password from config.json file.
    
    '''
    with open(CONFIG_PATH,"r") as config_file:
      self.config = ujson.load(config_file)
      # print(config)

    ssid = self.config['SSID']
    passwd = self.config['SSID_PASS']
    
    return ssid,passwd
    

  def _wifi_setup(self):
    '''
    If the default SSID and password can not make device connect to internet, then enable AP mode and hold a website on port 80 of the device. 
    User can type SSID name and password in the website. Ths SSID and password will be saved into local file and returned.


    
    '''
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='ESP32_'+self.config["DEV_ID"])
    
    Response.default_content_type = 'text/html'
    app=Microdot()
    @app.route('/', methods=['GET', 'POST'])
    def AP_index(request):
        if request.method == 'GET':
            return render_template('WiFi_setup.html',test='test')
        elif request.method == 'POST':
            ssid = request.form.get('SSID')
            ps = request.form.get('Pass')
            print(ssid,ps)
            self._save_SSID(ssid,ps)
            app.shutdown()
            ap.active(False)

            # return f"SSID:{ssid},pass:{ps}, server is shuting down.."
    
    @app.route('/src/<path:path>')
    def static(request, path):
        if '..' in path:
            # directory traversal is not allowed
            return 'Not found', 404
        return send_file('src/' + path)
    
    ap_netgate = ap.ifconfig()[0]
    self.oled.text(f"Set Wifi here:",0,20)
    self.oled.text(f"{ap_netgate}",0,30)
    ap_name = "ESP32_"+self.config["DEV_ID"]
    self.oled.text(f"in {ap_name}",0,40)

    self.oled.show()

    app.run(host='0.0.0.0',port=80,debug=True)


  
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

      max_attempts = 0
    while sta_if.isconnected()!=True and max_attempts<200:
      
      max_attempts+=1
      print(max_attempts)
      print("Connecting...")
      print(sta_if.isconnected())
    # print(sta_if.ifconfig()[0])
    # print(sta_if.isconnected())
    if sta_if.isconnected()==False:
      ## if user type a unavailable ssid, this will let them restart the device and try again
      self.oled.fill(0)
      unavailable_ssid = self.config["SSID"]
      self.oled.text(f"SSID:{unavailable_ssid}",0,0)
      self.oled.text(f"isn't available",0,10)
      self.oled.text(f"Please restart ",0,20)
      self.oled.text(f"the device and",0,30)
      self.oled.text(f"try again",0,40)
      self.oled.show()

      assert False, "Wifi is not available."



    print('network config:', sta_if.ifconfig())
    self.netconfig = sta_if.ifconfig()
    self.oled.fill(0)
    self.SHOW_NET_CONFIG=True
    self.oled.text("WiFi connected.",0,0)
    self.oled.text(f"{self.netconfig[0]}",0,20)
    self.oled.show()

  def _dht_init(self):
    # print(self.config)
    self.dht = dht.DHT22(machine.Pin(self.config["DHT_DATA_PIN"]))

  
  # def webserver(self):
  #   # html = """<!DOCTYPE html>
  #   # <html>
  #   #     <head> <title>ESP8266 Pins</title> </head>
  #   #     <body> <h1>ESP8266 Pins</h1>
  #   #         <p>Hello!</p>
  #   #     </body>
  #   # </html>
  #   # """
  #   with open(WIFI_SETUP_TEMPLATE,'r') as f:
  #     html = f.read()
  #   print(html)
  #   addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
  #   # 192.168.1.1:80
  #   # 192.168.1.1:80/setup_wifi.html
    
  #   s = socket.socket()
    
  #   s.bind(addr)
  #   s.listen(1)

  #   print('listening on', addr)
  #   while True:
  #       cl, addr = s.accept()
  #       print('client connected from', addr)
  #       cl_file = cl.makefile('rwb', 0)
  #       while True:
  #           line = cl_file.readline()
  #           if not line or line == b'\r\n':
  #               break
        
  #       response = html 
  #       cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
  #       cl.send(response)
  #       cl.close()
  

  def server(self):
    app=async_Microdot()

    @app.route('/', methods=['GET', 'POST'])
    async def server_index(request):
        if request.method == 'GET':
          
            # self.dht.measure() ## TODO: keep updating even without web user?
            return render_template('index.html',ip=self.netconfig[0])

    @app.route('/dht22', methods=['GET'])
    async def dht_enterpoint(request):
      self.dht.measure()
      self.oled.fill(0)
      if self.SHOW_NET_CONFIG==True:
            self.oled.text("WiFi connected.",0,0)
            self.oled.text(f"{self.netconfig[0]}",0,20)
      if self.SERVER_RUNNING==True:
            self.oled.text("Server is on:",0,10)

      self.oled.text(f"temp:{self.dht.temperature()}C",0,30)
      self.oled.text(f"hudi:{self.dht.humidity()}%",0,40)
      self.oled.show()
      dht_data = {
        'temperature':self.dht.temperature(),
        'humidity':self.dht.humidity(),

      }
      return dht_data
    
    # @app.route('/ifconfig', methods=['GET'])
    # def netconfig_enterpoint(request):
    #   netconfig = {
    #     'ip':self.netconfig[0]

    #   }
    #   return netconfig

    self.oled.text("Server is on:",0,10)
    self.oled.show()
    print("Running server..")
    self.SERVER_RUNNING=True

    # async def start_async_server():
    #   await app.start_server(host='0.0.0.0',port=80,debug=True)

    # asyncio.run(start_async_server())
    app.run(host='0.0.0.0',port=80,debug=True)
    

  def _oled_init(self):
    i2c = SoftI2C(scl=Pin(self.config["OLED_SCL"]), sda=Pin(self.config["OLED_SDA"]))
    oled_width = self.config["OLED_WIDTH"]
    oled_height = self.config["OLED_HEIGHT"]
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    self.oled = oled
    # oled.text("Connecting...",0,0)
    # oled.show()




def main():
  Response.default_content_type = 'text/html'


  smartoffice = SmartOfficeStation()
  smartoffice.server()
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
