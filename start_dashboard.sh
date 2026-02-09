#!/bin/bash
# Start a local web server for the Freqtrade Dashboard to avoid CORS issues
echo "Starting Freqtrade Commander Dashboard..."
echo "-----------------------------------------------------"
echo ">> OPEN YOUR BROWSER TO: http://localhost:8000"
echo "-----------------------------------------------------"
echo "Press Ctrl+C to stop the dashboard server."

# Check if python3 is available
if command -v python3 &>/dev/null; then
    python3 -m http.server 8000 --directory web_dashboard
else
    # Fallback to python if python3 not found
    python -m http.server 8000 --directory web_dashboard
fi
