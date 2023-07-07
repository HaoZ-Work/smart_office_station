#!/bin/bash

for device in /dev/ttyUSB*
do
    echo "*****Erase device: $device *****"
    esptool.py --chip esp32 --port $device erase_flash
    echo "*****Erase device: $device finished*****"

    echo "*****Install Micropython on device: $device *****"
    esptool.py --chip esp32 --port $device --baud 460800 write_flash -z 0x1000 esp32spiram-20220618-v1.19.1.bin
    echo "*****Install Micropython on device: $device finished *****"

    echo "*****Upload files to device: $device *****"
    for file in esp32_micropy/*
    do
        if [[ $file == *"config.json" ]]; then
            new_uuid=$(uuidgen)
            jq --arg uuid "$new_uuid" '.DEV_ID = $uuid' $file > "temp.json" && mv "temp.json" $file
        fi
        echo "Uploading file: $file to device: $device"
        ampy --port $device put $file
    done
    echo "*****Upload files to device: $device finished *****"
done
