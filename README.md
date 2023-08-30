## Smart office station
### 1. Set up development environment

#### (1) Download the micropython from http://www.micropython.org/download/esp32spiram/ , the current version is `v1.19.1 (2022-06-18)`
#### (2) Install micropython on ESP32 
>  esptool --chip esp32 --port /dev/ttyUSB0 erase_flash
>  esptool --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32spiram-20220618-v1.19.1.bin 

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

### 2. Set up env and transport code into a batch of devices. (Only tested on linux)
> Plug in all devices with USB Port
> run batch_setup.sh

#### Hardware requirement
> - Windows/Linux/Macos
> - ESP32
> - Sensors:Dht22,OLED monitor

#### To Use it in WSL2
> - [Set up usb connection in WSL2](https://learn.microsoft.com/zh-cn/windows/wsl/connect-usb)
> - sudo bash batch_setup.sh

### 3. Set up blink<1>

#### Clone and build the blink1-tool
```bash
git clone https://github.com/todbot/blink1-tool
cd blink1-tool
make
```
#### Install required libraries and rebuild
```bash
sudo apt-get install libusb-1.0-0-dev
make
```
#### Set up udev rules
```bash
wget https://github.com/todbot/blink1-tool/blob/main/51-blink1.rules
sudo udevadm control --reload
sudo udevadm trigger
```
#### Copy the tool and test the LED
```bash
cp blink1-tool/blink1-tool "$PATH:/home/..."
sudo blink1-tool --add_udev_rules
blink1-tool -m 100 --rgb=255,0,255
```
\```


##### Reference
> http://www.micropython.org/download/esp32/
> https://www.jianshu.com/p/9097920ea915
