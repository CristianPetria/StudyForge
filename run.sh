#!/bin/bash
# StudyForge Startup Script for Linux/Mac

echo ""
echo "=========================================="
echo "StudyForge - AI Study Guide Generator"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if requirements are installed
pip list | grep flask > /dev/null
if [ $? -ne 0 ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Copy .env.example to .env and configure your settings."
    echo ""
fi

echo ""
echo "Starting StudyForge API..."
python main.py
