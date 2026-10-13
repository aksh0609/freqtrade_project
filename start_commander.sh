#!/bin/bash

# Freqtrade Commander Web Dashboard Server
# Serves the web dashboard (default port 7100, outside the ports scalper uses)

PORT=${PORT:-7100}
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

# Refuse rather than kill whatever owns the port (it may be another project's server)
if nc -z 127.0.0.1 $PORT 2>/dev/null; then
    echo "❌ Port $PORT is already in use. Stop that process or run: PORT=<free port> $0"
    exit 1
fi

echo "🌐 Serving Freqtrade Commander at: http://$(hostname):$PORT"
echo "📝 Access this URL in your web browser to manage your bots."
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Use virtualenv uvicorn to serve the new backend app from root
./.venv/bin/uvicorn commander_server:app --host 0.0.0.0 --port $PORT
