#!/bin/bash

# VC Research Engine Setup Script

echo "=== VC Research Engine Setup ==="
echo "This script will install dependencies and set up the project."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 1
fi

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium
if [ $? -ne 0 ]; then
    echo "Error: Failed to install Playwright browsers."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
EOL
    echo "Please update the .env file with your API keys."
else
    echo ".env file already exists."
fi

echo ""
echo "=== Setup Complete ==="
echo "To run the API server:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Start the server: uvicorn main:app --reload"
echo "3. Access the API at: http://localhost:8000"
echo ""
echo "Don't forget to update your API keys in the .env file!"
