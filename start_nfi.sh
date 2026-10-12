#!/bin/bash

# Start Freqtrade NFI X7 Bot
# Port: 8083

cd "$(dirname "$0")"
PYTHON_ENV="$PWD/.venv/bin/python3"
CONFIG="user_data/config_nfi_8083.json"
STRATEGY="NostalgiaForInfinityX7"
LOG_FILE="/tmp/bot_8083.log"

echo "📊 Starting Bot 4: NFI X7 Strategy (Port 8083)..."

$PYTHON_ENV freqtrade trade -c $CONFIG --strategy $STRATEGY > $LOG_FILE 2>&1 &

PID=$!
echo "✅ Bot started with PID: $PID"
echo "📝 Logs: tail -f $LOG_FILE"
echo "🌐 Web UI: http://127.0.0.1:8083"
