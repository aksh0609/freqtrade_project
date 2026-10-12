#!/bin/bash
# Start Freqtrade with Bollinger Bands Strategy

echo "🛑 Stopping current bot..."
pkill -f "freqtrade trade"
sleep 2

echo "🚀 Starting Bollinger Bands Strategy..."
cd "$(dirname "$0")"
freqtrade trade -c user_data/config_bybit_spot.json --strategy BollingerBands_Strategy &

echo "✅ Bollinger Bands Strategy is now running!"
echo "📊 Access Web UI at: http://127.0.0.1:8080"
echo ""
echo "Strategy Details:"
echo "  - Entry: Price touches lower BB + RSI < 35"
echo "  - Exit: Price reaches middle BB or RSI > 70"
echo "  - Profit Target: 2.5%"
echo "  - Stop Loss: -1.5%"
