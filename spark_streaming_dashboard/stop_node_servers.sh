#!/bin/bash

# Function to kill all node processes
kill_all_node_processes() {
    local pids=$(ps aux | grep "node" | grep -v grep | awk '{print $2}')

    if [ -z "$pids" ]; then
        echo "No Node.js processes found"
    else
        for pid in $pids; do
            kill -9 $pid
            echo "Killed Node.js process with PID $pid"
        done
    fi
}

# Stop all Node.js processes
kill_all_node_processes

echo "All Node.js processes stopped"
