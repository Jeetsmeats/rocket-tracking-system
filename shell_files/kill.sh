#!/bin/bash

RPI1="10.13.124.175"
RPI2="10.12.42.202"
echo "Set up RPi IP Addresses"

# Function to kill all previous processes on remote Raspberry Pis by name
kill_remote_processes() {
    local RPI=$1
    ssh Jeetsmeats@$RPI "
        pkill -f 'mosquitto_sub';
        pkill -f 'ptp4l';
        pkill -f 'start.sh';
        pkill -f 'trigger_D.sh';
        pkill -f 'trigger_C.sh';
        pkill -f 'trigger_B.sh';
        pkill -f 'trigger_A.sh';
        pkill -f 'test_rpi.py';
        pkill -f 'test_rpi2.py';
    "
}

# Kill all previous relevant processes on both Raspberry Pis
kill_remote_processes $RPI1
kill_remote_processes $RPI2

echo "Killed all previous processes on both Raspberry Pis."
