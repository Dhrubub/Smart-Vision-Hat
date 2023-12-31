#!/bin/bash

# Log file
LOG_FILE="run.log"

# Initialize log file
echo "---- Starting Script ----" >$LOG_FILE

# Create .env in app/ if it doesn't exist
if [ ! -f "app/.env" ]; then
    echo "Creating .env file..." >>$LOG_FILE
    touch app/.env || {
        echo "Failed to create .env file." >>$LOG_FILE
        exit 1
    }
    # Initialize .env file
    echo "Initializing .env file..." >>$LOG_FILE
    echo "OPENAI_API_KEY=" >>app/.env

    # Ask user to type in OpenAI API key to .env or skip
    echo "Please enter your OpenAI API key or type 'skip' to proceed without it: "
    read OPENAI_API_KEY
    if [ "$OPENAI_API_KEY" != "skip" ]; then
        echo "OPENAI_API_KEY=$OPENAI_API_KEY" >app/.env || {
            echo "Failed to write API key to .env file." >>$LOG_FILE
            exit 1
        }
    else
        echo "Skipping OpenAI API key setup. Note: The 'ask' function will not be available."
    fi
fi

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

# Run Flask app in the background
echo "Running Flask app..." >>$LOG_FILE
flask run &
FLASK_PID=$!

# Sleep to ensure server starts
sleep 1

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

# Use trap to capture INT (Ctrl-C) signals and shut down Flask gracefully
trap "echo 'Stopping Flask app...'; kill $FLASK_PID" INT
wait $FLASK_PID

echo "---- Script Ended ----" >>$LOG_FILE
