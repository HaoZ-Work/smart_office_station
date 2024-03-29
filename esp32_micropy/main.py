import os
import urequests as requests
import network
import time
import ujson
import gc


try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

from machine import Pin, SoftI2C

import libs.ssd1306 as ssd1306

from microdot import Microdot, Response,send_file

from libs.microdot_asyncio import Microdot as async_Microdot

from libs.microdot_utemplate import render_template

# from libs.dht20 import DHT20
from libs.htu21d.htu21d import HTU21D as DHT20

CONFIG_PATH = './config.json'
# WIFI_SETUP_TEMPLATE = './WiFi_setup.html'
DHTRECORDING = './DHT_recording.csv' 

class SmartOfficeStation():
  '''
  This is the main class, new methods should be added here.
  '''
  def __init__(self) -> None:
     self._load_config()
     self._oled_init()
     self._wifi_connect()
     self._dht_init()
     self.SHOW_NET_CONFIG=True
     self.SERVER_RUNNING=True
     
     

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
      self.config["SSID_PASS"]=passwd
      self.config["SSID"] = ssid

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
        '''
        The enter point of wifi setup page, user can set up wifi here under ap mode.
        '''
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
        '''
        The path exposes the static resource file, like imgs or pics.
        '''
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
    '''
    Initialize the dht sensor 
    
    '''
    i2c0_sda = Pin(21)
    i2c0_scl = Pin(22)
    i2c0 = SoftI2C(sda=i2c0_sda, scl=i2c0_scl)

    self.dht = DHT20(i2c0)
    self.dht.measure()
 

    

    


  def server(self):
    '''
    a server application from microdot. It can hold the api and html page here.
    '''
    app=async_Microdot()

    @app.route('/', methods=['GET'])
    async def server_index(request):
      '''
      The enter point of main html page.
      '''
      if request.method == 'GET':
        return render_template('index.html',ip=self.netconfig[0])

    @app.route('/dht22', methods=['GET'])
    async def dht_enterpoint(request):
      '''
      The path for get data of dht22 sensor
      
      '''
      self.dht.measure()
      dht_data = {
        'temperature':self.dht.temperature(),
        'humidity':self.dht.humidity(),

      }

      return dht_data
  
    @app.route('/dht22/dumped', methods=['GET'])
    async def dht_return_dumped_data(request):
      '''
      The path for returning saved dht22 data from local json file.
      
      '''
      
      gc.collect()

      dht_recording = []
      with open(DHTRECORDING,'r') as file:
        for line in file:
          line_Str=file.readline()
          #print(line_Str)
          line_Str=line_Str.rstrip('\n')
          line_Str=line_Str.rstrip('\r')
          dht_recording.append(line_Str.split(','))
        file.close()



      self.print_memory_usage()

      # Take 42 points evenly from the list
      # dht_recording=dht_recording[::int(len(dht_recording)/42)]

      return dht_recording
  
    # set an endpoint to implement the pomodoro timer with variable pomodoro_time,
    @app.route('/pomodoro/<int:pomodoro_time>', methods=['GET'])
    async def pomodoro_enterpoint(request,pomodoro_time):
      '''
      When time goes up, it will show "Time is up!" and blink on the screen
      '''
      # fill the first three lines with black
      # set a counter to count down the time
      counter = pomodoro_time
      # Make the counter count down every second

      while counter >= 0:
        left_seconds = 60
        counter -= 1
        if counter <0:
          break
        while left_seconds >0:
          self.oled.fill_line(50,0)
          left_seconds -= 1
          self.oled.text(f"Time left:{counter}:{left_seconds}",0,50)

          self.oled.show()
          await asyncio.sleep(1) #time.sleep(1)
        
    
      for i in range(10):
        self.oled.fill_line(50,0)
        self.oled.text("Time is up!",0,50)
        self.oled.show()
        await asyncio.sleep(0.5)
        self.oled.fill_line(50,0)
        self.oled.show()
        await asyncio.sleep(0.5)
  
      return "Time is up!"
    

    # @app.route('/ifconfig', methods=['GET'])
    # def netconfig_enterpoint(request):
    #   netconfig = {
    #   }
    #   return netconfig







    async def start_async_server():
      '''
      This function wraps server and client. By using asyncio, they run simultaneously
      '''

      dump_client = self._client(self._dumpdht22,3600)
      task1 = asyncio.create_task(dump_client())

      query_client = self._client(self._querydht22,3)
      task3 = asyncio.create_task(query_client())

      wifi_checker = self._client(self._check_wifi_status,3)
      task4 = asyncio.create_task(wifi_checker())

      
      task2 = asyncio.create_task(app.run(host='0.0.0.0',port=80,debug=True))  

     
  
      await task1
      await task2
      await task3
      await task4

      
 
    #app.run(host='0.0.0.0',port=80,debug=True)


    asyncio.run(start_async_server())
    # print("end")
    


 

  def _client(self,func, delay):
    '''
    A client to hold some functions and make them run while server is running.
    Notice that, even it is called as client, but seems send request from here to server is not possible, unknown reason. 
    
    Args:
        func: the function to be wrapped
        delay: sleep time in seconds.
    
    '''
    print("Running client")

    async def wrapper():
      while True:
        # print("running wrapper")
        func()
        await asyncio.sleep(delay)    
       
    
    
    return wrapper


  def _check_wifi_status(self):
    sta_if = network.WLAN(network.STA_IF)
 
    if not sta_if.isconnected():
      self.SHOW_NET_CONFIG=False
      self.SERVER_RUNNING=False
 
  
  def _querydht22(self):
    '''
     This function will make device refresh data via dht22 and make them display on monitor
    '''
    self.dht.measure()
    self.currnet_temp = self.dht.temperature()
    self.current_hudi = self.dht.humidity()

    if self.SHOW_NET_CONFIG==True:
        self.oled.text("WiFi connected.",0,0)
        self.oled.text(f"{self.netconfig[0]}",0,20)
    else:
       self.oled.fill_line(0,0)
       self.oled.text("WiFi Disconnected.",0,0)
      #  self.oled.fill_line(20,0)
    if self.SERVER_RUNNING==True:

        self.oled.text("Server is on:",0,10)
    else:
        self.oled.fill_line(10,0)

        self.oled.text("Server is off:",0,10)
        self.oled.fill_line(20,0)
        self.oled.text("Please restart.",0,20)


    self.oled.fill_line(30,0)
    self.oled.fill_line(40,0)
    self.oled.text(f"temp:{self.currnet_temp}C",0,30)
    self.oled.text(f"hudi:{self.current_hudi}%",0,40)
    self.oled.show()

    
  
  
  
  
  def _dumpdht22(self):
    '''
    Write current data from dht22 sensor to json file.
    recording example: {'Fri 11:27:38': {'humidity': 35.4, 'temperature': 27.5}}
    '''
    weekday={
          "Sunday":"Sun",
          "Monday":"Mon",
          "Tuesday":"Tues",
          "Wednesday":"Wed",
          "Thursday":"Thur",
          "Friday":"Fri",
          "Saturday":"Sat"
    }
  
    csv_len = 0
    dht_recording=[]
    self.dht.measure()
    date = requests.get(url="https://www.timeapi.io/api/Time/current/zone?timeZone="+self.config["TIMEZONE"])
    date = weekday[date.json()['dayOfWeek']]+' '+ date.json()['time']

    new_data = date+","+ str(self.dht.temperature()) +","+ str(self.dht.humidity())
    print(f"new data:{new_data}")
    
    ## get the length of saved csv data
    with open(DHTRECORDING,"r") as dump_file:
        for line in dump_file:
          line_Str=dump_file.readline()
          #print(line_Str)
          line_Str=line_Str.rstrip('\n')
          line_Str=line_Str.rstrip('\r')
          # print(line_Str)
          dht_recording.append(line_Str.split(','))
          csv_len+=1
        #print(f"Loaded data:{dht_recording}")
        dump_file.close()


    print(f"len of csv:{csv_len}")
    CSV_MAXLEN = 168
    if csv_len >= CSV_MAXLEN:
      #print("---add/delete mode---")
      idx = 0
      with open(DHTRECORDING,"w") as dump_file:
        for line in dht_recording:
           if idx!=0:
              # print(line)
              line = line[0]+','+line[1]+','+line[2]
              # print(line)
              dump_file.write('\n'+line+'\n')
           idx+=1
        dump_file.write('\n'+new_data+'\n')
        dump_file.close()
    else:
      with open(DHTRECORDING,"a") as dump_file:
        print('Writing New data')
        dump_file.write('\n'+new_data+'\n') 
        #dump_file.close()
    

  def _oled_init(self):
    '''
    Initialized the olde monitor
    '''
    i2c = SoftI2C(scl=Pin(self.config["OLED_SCL"]), sda=Pin(self.config["OLED_SDA"]))

    oled_width = self.config["OLED_WIDTH"]
    oled_height = self.config["OLED_HEIGHT"]
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    self.oled = oled
  
  def print_memory_usage(self):
    free_memory = gc.mem_free()
    allocated_memory = gc.mem_alloc()
    total_memory = free_memory + allocated_memory

    print("Free memory: {} bytes".format(free_memory))
    print("Allocated memory: {} bytes".format(allocated_memory))
    print("Total memory: {} bytes".format(total_memory))
  




def main():
  Response.default_content_type = 'text/html'
  smartoffice = SmartOfficeStation()
  smartoffice.server()
  

if __name__ == '__main__':
  main()
