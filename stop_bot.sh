#!/bin/bash
# Stop Freqtrade Bot

echo "🛑 Stopping Freqtrade bot..."
pkill -f "freqtrade trade"
sleep 1

if pgrep -f "freqtrade trade" > /dev/null; then
    echo "❌ Bot is still running. Trying force stop..."
    pkill -9 -f "freqtrade trade"
    sleep 1
fi

if ! pgrep -f "freqtrade trade" > /dev/null; then
    echo "✅ Bot stopped successfully!"
else
    echo "⚠️  Could not stop bot. Please check manually."
fi
