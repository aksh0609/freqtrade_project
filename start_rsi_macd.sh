#!/bin/bash
# Start Freqtrade with RSI-MACD Strategy

echo "🛑 Stopping current bot..."
pkill -f "freqtrade trade"
sleep 2

echo "🚀 Starting RSI-MACD Strategy..."
cd /Users/akshaykumar/freqtrade
freqtrade trade -c user_data/config_bybit_spot.json --strategy RSI_MACD_Strategy &

echo "✅ RSI-MACD Strategy is now running!"
echo "📊 Access Web UI at: http://127.0.0.1:8080"
echo ""
echo "Strategy Details:"
echo "  - Entry: RSI < 30 + MACD bullish crossover"
echo "  - Exit: RSI > 70 + MACD bearish crossover"
echo "  - Profit Target: 3%"
echo "  - Stop Loss: -2%"
