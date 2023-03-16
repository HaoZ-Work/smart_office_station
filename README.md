## Smart office station
### Set up development environment

#### (1) Download the micropython from http://www.micropython.org/download/esp32/ , the current version is `v1.19.1 (2022-06-18)`
#### (2) Install micropython on ESP32 
>  esptool --chip esp32 --port /dev/ttyUSB0 erase_flash
>  esptool --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20220618-v1.19.1.bin

#### (3) Verify if Micropython is installed correctly.
>  Notice that the speed of rate should be `115200` instead of `9600` when you connect to port but see nothing.


#### (4) Set up coding environment:
> Download the vscode 
> Download the RT-Thread plugin: https://marketplace.visualstudio.com/items?itemName=RT-Thread.rt-thread-micropython#Introduction
> Use RT-Thread to connect to ESP32.

#### (5) Send the code from vscode in to ESP32
> Normally, it is noe necessary to change `boot.py`
> If you have a new folder to send, create the folder on ESP32 first. E.g. You want to send `src/image.png` to ESP32. First run `os.mkdir('src')` on ESP32 to create the path. Then send the `src` to ESP32. Once the files under `src` is changed, sync the whole `src` to ESP32 instead of only send changed file.

#### (6) Check the `config.json` of projeck and follow or change the port number of it to connect the ESP32 with sensors.


#### Hardware requirement
> - Windows/Linux/Macos
> - ESP32
> - Sensors:Dht22,OLED monitor


#### Reference
> http://www.micropython.org/download/esp32/
> https://www.jianshu.com/p/9097920ea915