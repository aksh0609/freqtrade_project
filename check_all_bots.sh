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
    echo "   Port 8080: http://127.0.0.1:8080  (Bollinger Bands)"
    echo "   Port 8081: http://127.0.0.1:8081  (RSI-MACD)"
    echo "   Port 8082: http://127.0.0.1:8082  (Manual Control)"
    echo "   Port 8083: http://127.0.0.1:8083  (NFI X7)"
    echo "   Port 8084: http://127.0.0.1:8084  (E0V1E_v17)"
    echo ""
    echo "👤 Login: freqtrader / freqtrade123"
    echo ""

    # Check API status
    echo "🔌 API Status:"
    curl -s http://127.0.0.1:8080/api/v1/ping > /dev/null 2>&1 && echo "   ✅ Port 8080: Online" || echo "   ❌ Port 8080: Offline"
    curl -s http://127.0.0.1:8081/api/v1/ping > /dev/null 2>&1 && echo "   ✅ Port 8081: Online" || echo "   ❌ Port 8081: Offline"
    curl -s http://127.0.0.1:8082/api/v1/ping > /dev/null 2>&1 && echo "   ✅ Port 8082: Online" || echo "   ❌ Port 8082: Offline"
    curl -s http://127.0.0.1:8083/api/v1/ping > /dev/null 2>&1 && echo "   ✅ Port 8083: Online" || echo "   ❌ Port 8083: Offline"
    curl -s http://127.0.0.1:8084/api/v1/ping > /dev/null 2>&1 && echo "   ✅ Port 8084: Online" || echo "   ❌ Port 8084: Offline"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
