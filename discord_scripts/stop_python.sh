#!/bin/bash

# Kill the process using the stored PID
if [ -f python_pid.txt ]; then
    kill $(cat python_pid.txt)
    rm python_pid.txt
    echo "Python script stopped."
else
    echo "No Python script running."
fi
