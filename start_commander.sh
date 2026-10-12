#!/bin/bash

# Freqtrade Commander Web Dashboard Server
# This script serves the web dashboard on port 8000

PORT=8000
DASHBOARD_DIR="$(cd "$(dirname "$0")" && pwd)/web_dashboard"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 STARTING FREQTRADE COMMANDER"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if dashboard dir exists
if [ ! -d "$DASHBOARD_DIR" ]; then
    echo "❌ Error: Dashboard directory not found at $DASHBOARD_DIR"
    exit 1
fi

# Check if port 8000 is already in use
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port $PORT is already in use."
    echo "Attempting to stop existing process on port $PORT..."
    lsof -ti :$PORT | xargs kill -9
    sleep 1
fi

echo "🌐 Serving Freqtrade Commander at: http://127.0.0.1:$PORT"
echo "📝 Access this URL in your web browser to manage your bots."
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Use virtualenv uvicorn to serve the new backend app from root
./.venv/bin/uvicorn commander_server:app --host 127.0.0.1 --port $PORT
