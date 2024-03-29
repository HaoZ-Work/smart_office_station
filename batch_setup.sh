#!/bin/bash
export PATH=$PATH:/home/ptw/.local/bin




# Function to set up each ESP32 device
set_device_1() {
    # The device port is passed as the first argument to the function
    device=$0
    # Indicate script beginning with red light
    blink1-tool -m 100 --rgb=255,0,0
    # Create a temporary directory for this device
    temp_dir="temp_$(basename $device)"
    mkdir -p $temp_dir
    cp -r esp32_micropy/* $temp_dir/

    # Record the start time
    start_time=$(date +%s)

    echo "*****Erasing device: $device *****"
    # Use esptool.py to erase the flash memory of the device
    esptool.py --chip esp32 --port $device erase_flash
    echo "*****Erasing device: $device finished*****"

    #echo "*****Installing Micropython on device: $device *****"
    ## Install Micropython on the device
    #esptool.py --chip esp32 --port $device --baud 460800 write_flash -z 0x1000 esp32spiram-20220618-v1.19.1.bin
    #echo "*****Installing Micropython on device: $device finished *****"

    #esptool.py --port /dev/ttyUSB0 erase_flash
    esptool.py --chip esp32 --port $device --baud 115200 write_flash 0x00000 esp32_dump.bin
    echo "*****Uploading files to device: $device *****"
    # Iterate over all files in the temp directory
    for file in $temp_dir/*
    do
        # If the file is config.json, generate a new UUID and replace the DEV_ID field in the file
        if [[ $file == *"config.json" ]]; then
            new_uuid=$(uuidgen)
            jq --arg uuid "$new_uuid" '.DEV_ID = $uuid' $file > "$temp_dir/temp.json" && mv "$temp_dir/temp.json" $file
            ampy --port $device put $temp_dir/config.json

            if [ $? -eq 0 ]; then
                # Indicate script completion with green light
                blink1-tool -m 100 --rgb=0,255,0
            fi
        fi

           # Skip files ending in .original
        if [[ $file == *.original ]]; then
            continue
        fi

        # Upload the file to the device
    #    echo "Uploading file: $file to device: $device"
    #    ampy --port $device put $file
    done
    
    
    # Record the end time and calculate the elapsed time
    end_time=$(date +%s)
    echo "*****Uploading files to device: $device finished *****"
    echo "Time taken: $(($end_time - $start_time)) seconds"
    # Remove the temporary directory
    rm -rf $temp_dir
}


set_device_2() {
    # The device port is passed as the first argument to the function
    device=$0
    blink1-tool -m 100 --rgb=255,0,0
    # Create a temporary directory for this device
    temp_dir="temp_$(basename $device)"
    mkdir -p $temp_dir
    cp -r esp32_micropy/* $temp_dir/
    # Record the start time
    start_time=$(date +%s)

    echo "*****Erasing device: $device *****"

    # Use esptool.py to erase the flash memory of the device
    esptool.py --chip esp32 --port $device erase_flash
    echo "*****Erasing device: $device finished*****"

    echo "*****Installing Micropython on device: $device *****"
    # Install Micropython on the device
    esptool.py --chip esp32 --port $device --baud 460800 write_flash -z 0x1000 esp32spiram-20220618-v1.19.1.bin
    echo "*****Installing Micropython on device: $device finished *****"

    echo "*****Uploading files to device: $device *****"
    # Iterate over all files in the temp directory
    for file in $temp_dir/*
    do
        # If the file is config.json, generate a new UUID and replace the DEV_ID field in the file
        if [[ $file == *"config.json" ]]; then
            new_uuid=$(uuidgen)
            jq --arg uuid "$new_uuid" '.DEV_ID = $uuid' $file > "$temp_dir/temp.json" && mv "$temp_dir/temp.json" $file
        fi

           # Skip files ending in .original
        if [[ $file == *.original ]]; then
            continue
        fi

        # Upload the file to the device
        echo "Uploading file: $file to device: $device"
        ampy --port $device put $file
           
 
    done 
    blink1-tool -m 100 --rgb=0,255,0
    # Record the end time and calculate the elapsed time
    end_time=$(date +%s)
    echo "*****Uploading files to device: $device finished *****"
    echo "Time taken: $(($end_time - $start_time)) seconds"

    # Remove the temporary directory
    rm -rf $temp_dir
}

if [[ "$1" == "--from" && "$2" == "file" ]]; then
    FUNCTION_TO_CALL="set_device_2"
else
    FUNCTION_TO_CALL="set_device_1"
fi

# Record the start time of the whole script
SECONDS=0

# Check if the system is Debian-based or RHEL-based
if [ -f /etc/debian_version ]; then
    PACKAGE_MANAGER="apt-get"
else
    PACKAGE_MANAGER="yum"
fi

# # Install necessary packages if they are not already installed
# for program in jq uuidgen python3 python3-pip; do
#     if ! which $program > /dev/null; then
#         echo "Installing $program..."
#         sudo $PACKAGE_MANAGER install -y $program
#     fi
# done

# # Check if the necessary Python packages are installed, install if not
# for package in esptool adafruit-ampy; do
#     if ! pip list --format=columns | grep -i $package > /dev/null; then
#         echo "Installing Python package $package..."
#         pip install $package
#     fi
# done

# Get the number of devices for parallel processing
device_num=$(ls /dev/ttyUSB* | wc -l)
echo "Number of devices: $device_num"


# Export the function for use in xargs
export -f set_device_1
export -f set_device_2


# Set the PATH environment variable
echo PATH="$HOME/bin:$HOME/.local/bin:$PATH"
# Iterate over all devices in parallel, calling the chosen function for each one

ls /dev/ttyUSB* | xargs -n 1 -P $device_num bash -c "$FUNCTION_TO_CALL "'"$0"'



# Print the total time taken by the script
echo "Total time taken: $SECONDS seconds"

