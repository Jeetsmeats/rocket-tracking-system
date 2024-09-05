#!/bin/bash

RPI1="10.13.124.175"
RPI2="10.12.42.202"
echo "Set up RPi IP Addresses"

# Function to kill all previous processes on remote Raspberry Pis by name
kill_remote_processes() {
    local RPI=$1
    ssh Jeetsmeats@$RPI "sudo killall hackrf_transfer ptp4l python3"
}

# Kill all previous relevant processes on both Raspberry Pis
kill_remote_processes $RPI1
kill_remote_processes $RPI2

echo "Killed all previous processes on both Raspberry Pis."