#!/bin/bash
# Start All Bots Simultaneously

echo "🚀 Starting All Freqtrade Bots..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$(dirname "$0")"

# Start Bot 1: Bollinger Bands on Port 7101
echo "📊 Starting Bot 1: Bollinger Bands Strategy (Port 7101)..."
./.venv/bin/freqtrade trade -c user_data/config_bollinger_7101.json --strategy BollingerBands_Strategy > /tmp/bot_7101.log 2>&1 &
BOT1_PID=$!
sleep 2

# Start Bot 2: RSI-MACD on Port 7102
echo "📊 Starting Bot 2: RSI-MACD Strategy (Port 7102)..."
./.venv/bin/freqtrade trade -c user_data/config_rsi_macd_7102.json --strategy RSI_MACD_Strategy > /tmp/bot_7102.log 2>&1 &
BOT2_PID=$!
sleep 2

# Start Bot 3: Manual Control on Port 7103
echo "📊 Starting Bot 3: Manual Control Strategy (Port 7103)..."
./.venv/bin/freqtrade trade -c user_data/config_scalper_7103.json --strategy Manual_Control_Strategy > /tmp/bot_7103.log 2>&1 &
BOT3_PID=$!
sleep 2

# Start Bot 4: NFI X7 on Port 7104
echo "📊 Starting Bot 4: NFI X7 Strategy (Port 7104)..."
./.venv/bin/freqtrade trade -c user_data/config_nfi_7104.json --strategy NostalgiaForInfinityX7 > /tmp/bot_7104.log 2>&1 &
BOT4_PID=$!
sleep 2

# Start Bot 5: E0V1E_v17 on Port 7105
echo "📊 Starting Bot 5: E0V1E_v17 Strategy (Port 7105)..."
./.venv/bin/freqtrade trade -c user_data/config_e0v1e_7105.json --strategy E0V1E_v17 > /tmp/bot_7105.log 2>&1 &
BOT5_PID=$!
sleep 2

# Start Bot 6: Dip Catcher on Port 7106
echo "📊 Starting Bot 6: Dip Catcher Strategy (Port 7106)..."
./.venv/bin/freqtrade trade -c user_data/config_dip_catcher_7106.json --strategy DipDetectionStrategy > /tmp/bot_7106.log 2>&1 &
BOT6_PID=$!
sleep 2

# Start Bot 7: Michael Harris on Port 7107
echo "📊 Starting Bot 7: Michael Harris Strategy (Port 7107)..."
./.venv/bin/freqtrade trade -c user_data/config_mh_7107.json --strategy MichaelHarrisStrategy > /tmp/bot_7107.log 2>&1 &
BOT7_PID=$!
sleep 2

# Start Bot 8: Fear Trader on Port 7108
echo "📊 Starting Bot 8: Fear Trader Strategy (Port 7108)..."
./.venv/bin/freqtrade trade -c user_data/config_fear_7108.json --strategy BollingerBounceFearTrader > /tmp/bot_7108.log 2>&1 &
BOT8_PID=$!
sleep 2

echo ""
echo "✅ All Bots Started!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Bot Status:"
echo "  Bot 1 (Bollinger)      - PID: $BOT1_PID - http://127.0.0.1:7101"
echo "  Bot 2 (RSI-MACD)       - PID: $BOT2_PID - http://127.0.0.1:7102"
echo "  Bot 3 (Manual Control) - PID: $BOT3_PID - http://127.0.0.1:7103"
echo "  Bot 4 (NFI X7)         - PID: $BOT4_PID - http://127.0.0.1:7104"
echo "  Bot 5 (E0V1E_v17)      - PID: $BOT5_PID - http://127.0.0.1:7105"
echo "  Bot 6 (Dip Catcher)    - PID: $BOT6_PID - http://127.0.0.1:7106"
echo "  Bot 7 (MH Pattern)     - PID: $BOT7_PID - http://127.0.0.1:7107"
echo "  Bot 8 (Fear Trader)    - PID: $BOT8_PID - http://127.0.0.1:7108"
echo ""
echo "🌐 Access Web UIs:"
echo "  Bollinger:      http://127.0.0.1:7101"
echo "  RSI-MACD:       http://127.0.0.1:7102"
echo "  Manual Control: http://127.0.0.1:7103"
echo "  NFI X7:         http://127.0.0.1:7104"
echo "  E0V1E_v17:      http://127.0.0.1:7105"
echo "  Dip Catcher:    http://127.0.0.1:7106"
echo "  MH Pattern:     http://127.0.0.1:7107"
echo "  Fear Trader:    http://127.0.0.1:7108"
echo ""
echo "👤 Login: freqtrader / freqtrade123"
echo ""
echo "📝 View Logs:"
echo "  tail -f /tmp/bot_7101.log  # Bollinger"
echo "  tail -f /tmp/bot_7102.log  # RSI-MACD"
echo "  tail -f /tmp/bot_7103.log  # Manual Control"
echo "  tail -f /tmp/bot_7104.log  # NFI X7"
echo "  tail -f /tmp/bot_7105.log  # E0V1E_v17"
echo "  tail -f /tmp/bot_7106.log  # Dip Catcher"
echo "  tail -f /tmp/bot_7107.log  # MH Pattern"
echo "  tail -f /tmp/bot_7108.log  # Fear Trader"
echo ""
echo "🛑 To stop all bots: ./stop_all_bots.sh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
