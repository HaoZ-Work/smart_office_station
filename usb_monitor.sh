#!/bin/bash

LOG_FILE="/home/ptw/Schreibtisch/smart/smart_office_station/logfile.log"

echo "Script started" >> $LOG_FILE

prev_devices=$(ls /dev | grep ttyUSB | wc -l)


blink_executed=false

while true; do
    current_devices=$(ls /dev | grep ttyUSB | wc -l)

    if (( current_devices > prev_devices )) && $blink_executed; then
        echo "USB device added at $(date)" >> $LOG_FILE
        sudo -u ptw bash -c "cd /home/ptw/Schreibtisch/smart/smart_office_station; bash batch_setup.sh"  #>> $LOG_FILE 2>&1
        blink_executed=false
    elif (( current_devices == prev_devices )); then
        blink1-tool -m 100 --rgb=255,255,255
        blink_executed=true
    fi

    #prev_devices=$current_devices
    sleep 1
done
