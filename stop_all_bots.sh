#!/bin/bash
# Stop All Running Freqtrade Bots

echo "🛑 Stopping All Freqtrade Bots..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "🛑 Stopping Bot 1 (Bollinger)..."
pkill -f "config_bollinger_8080.json"
echo "🛑 Stopping Bot 2 (RSI-MACD)..."
pkill -f "config_rsi_macd_8081.json"
echo "🛑 Stopping Bot 3 (Manual Control)..."
pkill -f "config_scalper_8082.json"
echo "🛑 Stopping Bot 4 (NFI X7)..."
pkill -f "config_nfi_8083.json"
echo "🛑 Stopping Bot 5 (E0V1E_v17)..."
pkill -f "config_e0v1e_8084.json"
echo "🛑 Stopping Bot 6 (Dip Catcher)..."
pkill -f "config_dip_catcher_8085.json"
echo "🛑 Stopping Bot 7 (MH Pattern)..."
pkill -f "config_mh_8086.json"

sleep 2

# Check if any are still running
if pgrep -f "freqtrade trade" > /dev/null; then
    echo "⚠️  Some bots still running. Force stopping..."
    pkill -9 -f "freqtrade trade"
    sleep 1
fi

# Verify all stopped
if ! pgrep -f "freqtrade trade" > /dev/null; then
    echo "✅ All bots stopped successfully!"
else
    echo "❌ Could not stop all bots. Please check manually."
    ps aux | grep "freqtrade trade" | grep -v grep
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
