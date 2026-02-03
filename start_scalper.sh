#!/bin/bash

# Start Freqtrade Scalper Bot (Manual Control)
# Port: 8082

PYTHON_ENV="/Users/akshaykumar/freqtrade/.venv/bin/python3"
CONFIG="user_data/config_scalper_8082.json"
STRATEGY="ManualControlStrategy"
LOG_FILE="/tmp/bot_8082.log"

echo "📊 Starting Bot 3: Manual Control Strategy (Port 8082)..."

$PYTHON_ENV freqtrade trade -c $CONFIG --strategy $STRATEGY > $LOG_FILE 2>&1 &

PID=$!
echo "✅ Bot started with PID: $PID"
echo "📝 Logs: tail -f $LOG_FILE"
echo "🌐 Web UI: http://127.0.0.1:8082"
