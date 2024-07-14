#!/bin/bash

# Find the PID of the python script named discord_boy.py and kill it
pids=$(pgrep -f discord_bot.py)

if [ -z "$pids" ]; then
    echo "No Python script named discord_bot.py is running."
else
    echo "Found the following PIDs for discord_boy.py: $pids"
    for pid in $pids; do
        echo "Killing Python script with PID $pid."
        kill $pid
    done
    echo "All specified Python scripts have been stopped."
fi
