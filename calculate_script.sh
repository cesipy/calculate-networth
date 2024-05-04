#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment 'venv' not found. Please create it first."
    exit 1
fi

source venv/bin/activate
python src/main.py --plot       #run 
deactivate
