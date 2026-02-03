#!/bin/bash
# Start Bot 5: E0V1E_v17 on Port 8084

echo "📊 Starting Bot 5: E0V1E_v17 (Port 8084)..."
cd /Users/akshaykumar/freqtrade

# Use virtual environment python to run freqtrade
./.venv/bin/freqtrade trade -c user_data/config_e0v1e_8084.json --strategy E0V1E_v17 > /tmp/bot_8084.log 2>&1 &

PID=$!
echo "✅ Bot 5 started with PID: $PID"
echo "🌐 Web UI: http://127.0.0.1:8084"
echo "👤 Login: freqtrader / freqtrade123"
echo "📝 View logs: tail -f /tmp/bot_8084.log"
