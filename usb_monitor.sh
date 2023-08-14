#!/bin/bash

#!/bin/bash

LOG_FILE="/home/ptwadmin/Desktop/smart_office_station/logfile.log"

echo "Script started" >> $LOG_FILE

prev_devices=$(ls /dev | grep ttyUSB | wc -l)

while true; do
    current_devices=$(ls /dev | grep ttyUSB | wc -l)

    if (( current_devices > prev_devices )); then
        echo "USB device added at $(date)" >> $LOG_FILE
        echo -e "\a"
        sleep 3
        su - ptwadmin -c "cd /home/ptwadmin/Desktop/smart_office_station; bash batch_setup.sh"  #>> $LOG_FILE 2>&1
    fi

    prev_devices=$current_devices
    sleep 1
done



