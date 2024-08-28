#!/bin/bash

RPI1="10.13.124.175"
RPI2="10.12.42.202"

run_command() {
	
	local RPI=$1
	local COMMAND=$2

	ssh Jeetsmeats@$RPI "$COMMAND"
}

# Subscribe to test/topic in background
mosquitto_sub -d -t "test/topic" 

# Start HackRF B Internal Clock
run_command $RPI1 "bash /Documents/rocket-tracking-system/shell_files/start.sh"

# Set up Raspberry Pi 1 as PTP master
run_command $RPI1 "bash sudo ptp4l -i eth0 --masterOnly 1 -m --tx_timestamp_timeout 200"
sleep(1)

# Set up Raspberry Pi 2 as PTP slave
run_command $RPI2 "bash sudo ptp4l -i eth0 --slaveOnly 1 -m --tx_timestamp_timeout 200"

sleep(30)

# Run HackRF D trigger
run_command $RPI2 "bash /Documents/rocket-tracking-system/shell_files/trigger_D.sh"
sleep(1)

# Run HackRF C trigger
run_command $RPI2 "bash /Documents/rocket-tracking-system/shell_files/trigger_C.sh"
sleep(1)

# Run Hack B and A trigger
(run_command $RPI1 "bash /Documents/rocket-tracking-system/shell_files/trigger_A.sh") &
(run_command $RPI1 "bash /Documents/rocket-tracking-system/shell_files/trigger_B.sh") &
sleep(0.5)

# Run Data Acquisition Files
(run_command $RPI1 "python3 /Documents/rocket-tracking-system/test_files/test_rpi.py") &
(run_command $RPI2 "python3 /Documents/rocket-tracking-system/test_files/test_rpi2.py) &


