#!/bin/bash
# Check Status of All Running Bots

echo "🔍 Checking All Freqtrade Bots Status..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Count running bots
BOT_COUNT=$(pgrep -f "freqtrade trade" | wc -l | tr -d ' ')

if [ "$BOT_COUNT" -eq 0 ]; then
    echo "❌ No bots are currently running"
    echo ""
    echo "To start all bots: ./start_all_bots.sh"
else
    echo "✅ Found $BOT_COUNT bot(s) running"
    echo ""

    # List all running bots
    ps aux | grep "freqtrade trade" | grep -v grep | while read line; do
        PID=$(echo $line | awk '{print $2}')
        CONFIG=$(echo $line | grep -o "config_[^ ]*\.json" || echo "unknown")
        STRATEGY=$(echo $line | grep -o "\-\-strategy [^ ]*" | cut -d' ' -f2 || echo "unknown")

        echo "📊 Bot Details:"
        echo "   PID: $PID"
        echo "   Config: $CONFIG"
        echo "   Strategy: $STRATEGY"
        echo ""
    done

    echo "🌐 Web UI Access:"
    echo "   Port 7101: http://127.0.0.1:7101  (Bollinger Bands)"
    echo "   Port 7102: http://127.0.0.1:7102  (RSI-MACD)"
    echo "   Port 7103: http://127.0.0.1:7103  (Manual Control)"
    echo "   Port 7104: http://127.0.0.1:7104  (NFI X7)"
    echo "   Port 7105: http://127.0.0.1:7105  (E0V1E_v17)"
    echo ""
    echo "👤 Login: freqtrader / freqtrade123"
    echo ""

    # Check API status
    echo "🔌 API Status:"
    curl -s http://127.0.0.1:7101/api/v1/ping > /dev/null 2>&1 && echo "   ✅ Port 7101: Online" || echo "   ❌ Port 7101: Offline"
    curl -s http://127.0.0.1:7102/api/v1/ping > /dev/null 2>&1 && echo "   ✅ Port 7102: Online" || echo "   ❌ Port 7102: Offline"
    curl -s http://127.0.0.1:7103/api/v1/ping > /dev/null 2>&1 && echo "   ✅ Port 7103: Online" || echo "   ❌ Port 7103: Offline"
    curl -s http://127.0.0.1:7104/api/v1/ping > /dev/null 2>&1 && echo "   ✅ Port 7104: Online" || echo "   ❌ Port 7104: Offline"
    curl -s http://127.0.0.1:7105/api/v1/ping > /dev/null 2>&1 && echo "   ✅ Port 7105: Online" || echo "   ❌ Port 7105: Offline"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
