#!/bin/bash

RPI1="10.13.124.175"
RPI2="10.12.42.202"
echo "Set up RPi IP Addresses"

run_command() {
	
	local RPI=$1
	local COMMAND=$2

	ssh Jeetsmeats@$RPI "$COMMAND"
}



# Start HackRF B Internal Clock
run_command $RPI1 "bash ~/Documents/rocket-tracking-system/shell_files/start.sh"
echo "Activated HackRF B master clock"

# Set up Raspberry Pi 1 as PTP master, run as P2P instead of E2E
run_command $RPI1 "bash sudo ptp4l -i eth0 -m 1 -P"
sleep 1s
echo "Set up PTP master Raspberry Pi 1"

# Set up Raspberry Pi 2 as PTP slave
run_command $RPI2 "bash sudo ptp4l -i eth0 -m 0 -P"
echo "Set up PTP slave Raspberry Pi 2, awaiting synchronisation completion..."
sleep 15s

# Run HackRF D trigger
run_command $RPI2 "bash ~/Documents/rocket-tracking-system/shell_files/trigger_D.sh"
sleep 1s
echo "Triggered HackRF D!"

# Run HackRF C trigger
run_command $RPI2 "bash ~/Documents/rocket-tracking-system/shell_files/trigger_C.sh"
sleep 1s
echo "Trigger HackRF C!"

# Run Hack B and A trigger
(run_command $RPI1 "bash ~/Documents/rocket-tracking-system/shell_files/trigger_A.sh") &
(run_command $RPI1 "bash ~/Documents/rocket-tracking-system/shell_files/trigger_B.sh") &
sleep 1s
echo "Trigger HackRF B and C!"

# Run Data Acquisition Files
(run_command $RPI1 "~Documents/rocket-tracking-system/.venv/bin/python3 ~/Documents/rocket-tracking-system/test_files/test_rpi.py") &
(run_command $RPI2 "~Documents/rocket-tracking-system/.venv/bin/python3 ~/Documents/rocket-tracking-system/test_files/test_rpi2.py) &
echo "Executed data collection files and collecting data!"