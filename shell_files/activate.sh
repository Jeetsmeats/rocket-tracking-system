#!/bin/bash

RPI1="10.13.101.198"
RPI2="10.12.48.240"
echo "Set up RPi IP Addresses"

run_command() {
    local RPI=$1
    local COMMAND=$2
    ssh Jeetsmeats@$RPI "$COMMAND" > /dev/null &
}

# Start HackRF B Internal Clock
run_command $RPI1 "bash ~/Documents/rocket-tracking-system/shell_files/start.sh"
echo "Activated HackRF B master clock"

# Set up Raspberry Pi 1 as PTP master, run as P2P instead of E2E
run_command $RPI1 "sudo ptp4l -i eth0 -m 1 -P" &
sleep 10s
echo "Set up PTP master Raspberry Pi 1"

# Set up Raspberry Pi 2 as PTP slave
run_command $RPI2 "sudo ptp4l -i eth0 -m 0 -P" &
echo "Set up PTP slave Raspberry Pi 2, awaiting synchronisation completion..."
sleep 15s

# Run HackRF D trigger
run_command $RPI2 "bash ~/Documents/rocket-tracking-system/shell_files/trigger_D.sh" &
echo "Triggered HackRF D!"

# Run HackRF C trigger
run_command $RPI2 "bash ~/Documents/rocket-tracking-system/shell_files/trigger_C.sh" &
echo "Trigger HackRF C!"

# Run HackRF B trigger
run_command $RPI1 "bash ~/Documents/rocket-tracking-system/shell_files/trigger_B.sh" &

echo "Trigger HackRF B!"

# Run HackRF A trigger
run_command $RPI1 "bash ~/Documents/rocket-tracking-system/shell_files/trigger_A.sh" &

echo "Trigger HackRF A!"

# Run the receiver code
(run_command $RPI1 "~/Documents/rocket-tracking-system/.venv/bin/python3 ~/Documents/rocket-tracking-system/receiver2x2.py" &

# Run Data Acquisition Files
(run_command $RPI2 "~/Documents/rocket-tracking-system/.venv/bin/python3 ~/Documents/rocket-tracking-system/test_files/test_rpi2.py") &
sleep 5s
(run_command $RPI1 "~/Documents/rocket-tracking-system/.venv/bin/python3 ~/Documents/rocket-tracking-system/test_files/test_rpi.py") &

echo "Executed data collection files and collecting data!"
