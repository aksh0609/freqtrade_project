#!/bin/bash
# Check Freqtrade Bot Status

echo "🔍 Checking Freqtrade Bot Status..."
echo ""

if pgrep -f "freqtrade trade" > /dev/null; then
    echo "✅ Bot is RUNNING"
    echo ""

    # Get the strategy name
    STRATEGY=$(ps aux | grep "freqtrade trade" | grep -v grep | grep -o "\-\-strategy [^ ]*" | cut -d' ' -f2)

    if [ -n "$STRATEGY" ]; then
        echo "📊 Active Strategy: $STRATEGY"
    fi

    echo "Process Details:"
    ps aux | grep "freqtrade trade" | grep -v grep | awk '{print "  PID: "$2" | CPU: "$3"% | Memory: "$4"%"}'

    echo ""
    echo "🌐 Web UI Access:"
    echo "  Bollinger:      http://127.0.0.1:8080"
    echo "  RSI-MACD:       http://127.0.0.1:8081"
    echo "  Manual Control: http://127.0.0.1:8082"
    echo "  NFI X7:         http://127.0.0.1:8083"
    echo ""
    echo "👤 Username: freqtrader"
    echo "🔑 Password: freqtrade123"

else
    echo "❌ Bot is NOT running"
    echo ""
    echo "To start all bots, run: ./start_all_bots.sh"
    echo "To start individual bots, run:"
    echo "  ./start_bollinger.sh"
    echo "  ./start_rsi_macd.sh"
    echo "  ./start_scalper.sh"
    echo "  ./start_nfi.sh"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
