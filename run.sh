#!/bin/bash

# Log file
LOG_FILE="run.log"

# Initialize log file
echo "---- Starting Script ----" >$LOG_FILE

# Check if venv exists; if not, create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..." >>$LOG_FILE
    python3 -m venv venv || {
        echo "Failed to create venv." >>$LOG_FILE
        exit 1
    }
fi

# Activate virtual environment
echo "Activating virtual environment..." >>$LOG_FILE
source venv/bin/activate || {
    echo "Failed to activate venv." >>$LOG_FILE
    exit 1
}

# Install dependencies
echo "Installing dependencies..." >>$LOG_FILE
pip install -r requirements.txt || {
    echo "Failed to install dependencies." >>$LOG_FILE
    exit 1
}

# Check port availability
if netstat -tuln | grep -q ':5000\s'; then
    echo "Port 5000 is busy." >>$LOG_FILE
    exit 1
fi

# Run Flask app
echo "Running Flask app..." >>$LOG_FILE
flask run &

# Sleep to ensure server starts
sleep 3

# Open URL based on OS
echo "Opening browser..." >>$LOG_FILE
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://127.0.0.1:5000
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open http://127.0.0.1:5000
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    start http://127.0.0.1:5000
else
    echo "OS not supported" >>$LOG_FILE
    exit 1
fi

echo "---- Script Ended ----" >>$LOG_FILE
