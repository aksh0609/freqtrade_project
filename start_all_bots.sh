#!/bin/bash
# Start All Bots Simultaneously

echo "🚀 Starting All Freqtrade Bots..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd /Users/akshaykumar/freqtrade

# Start Bot 1: Bollinger Bands on Port 8080
echo "📊 Starting Bot 1: Bollinger Bands Strategy (Port 8080)..."
./.venv/bin/freqtrade trade -c user_data/config_bollinger_8080.json --strategy BollingerBands_Strategy > /tmp/bot_8080.log 2>&1 &
BOT1_PID=$!
sleep 2

# Start Bot 2: RSI-MACD on Port 8081
echo "📊 Starting Bot 2: RSI-MACD Strategy (Port 8081)..."
./.venv/bin/freqtrade trade -c user_data/config_rsi_macd_8081.json --strategy RSI_MACD_Strategy > /tmp/bot_8081.log 2>&1 &
BOT2_PID=$!
sleep 2

# Start Bot 3: Manual Control on Port 8082
echo "📊 Starting Bot 3: Manual Control Strategy (Port 8082)..."
./.venv/bin/freqtrade trade -c user_data/config_scalper_8082.json --strategy Manual_Control_Strategy > /tmp/bot_8082.log 2>&1 &
BOT3_PID=$!
sleep 2

# Start Bot 4: NFI X7 on Port 8083
echo "📊 Starting Bot 4: NFI X7 Strategy (Port 8083)..."
./.venv/bin/freqtrade trade -c user_data/config_nfi_8083.json --strategy NostalgiaForInfinityX7 > /tmp/bot_8083.log 2>&1 &
BOT4_PID=$!
sleep 2

# Start Bot 5: E0V1E_v17 on Port 8084
echo "📊 Starting Bot 5: E0V1E_v17 Strategy (Port 8084)..."
./.venv/bin/freqtrade trade -c user_data/config_e0v1e_8084.json --strategy E0V1E_v17 > /tmp/bot_8084.log 2>&1 &
BOT5_PID=$!
sleep 2

# Start Bot 6: Dip Catcher on Port 8085
echo "📊 Starting Bot 6: Dip Catcher Strategy (Port 8085)..."
./.venv/bin/freqtrade trade -c user_data/config_dip_catcher_8085.json --strategy DipDetectionStrategy > /tmp/bot_8085.log 2>&1 &
BOT6_PID=$!
sleep 2

# Start Bot 7: Michael Harris on Port 8086
echo "📊 Starting Bot 7: Michael Harris Strategy (Port 8086)..."
./.venv/bin/freqtrade trade -c user_data/config_mh_8086.json --strategy MichaelHarrisStrategy > /tmp/bot_8086.log 2>&1 &
BOT7_PID=$!
sleep 2

# Start Bot 8: Fear Trader on Port 8087
echo "📊 Starting Bot 8: Fear Trader Strategy (Port 8087)..."
./.venv/bin/freqtrade trade -c user_data/config_fear_8087.json --strategy BollingerBounceFearTrader > /tmp/bot_8087.log 2>&1 &
BOT8_PID=$!
sleep 2

echo ""
echo "✅ All Bots Started!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Bot Status:"
echo "  Bot 1 (Bollinger)      - PID: $BOT1_PID - http://127.0.0.1:8080"
echo "  Bot 2 (RSI-MACD)       - PID: $BOT2_PID - http://127.0.0.1:8081"
echo "  Bot 3 (Manual Control) - PID: $BOT3_PID - http://127.0.0.1:8082"
echo "  Bot 4 (NFI X7)         - PID: $BOT4_PID - http://127.0.0.1:8083"
echo "  Bot 5 (E0V1E_v17)      - PID: $BOT5_PID - http://127.0.0.1:8084"
echo "  Bot 6 (Dip Catcher)    - PID: $BOT6_PID - http://127.0.0.1:8085"
echo "  Bot 7 (MH Pattern)     - PID: $BOT7_PID - http://127.0.0.1:8086"
echo "  Bot 8 (Fear Trader)    - PID: $BOT8_PID - http://127.0.0.1:8087"
echo ""
echo "🌐 Access Web UIs:"
echo "  Bollinger:      http://127.0.0.1:8080"
echo "  RSI-MACD:       http://127.0.0.1:8081"
echo "  Manual Control: http://127.0.0.1:8082"
echo "  NFI X7:         http://127.0.0.1:8083"
echo "  E0V1E_v17:      http://127.0.0.1:8084"
echo "  Dip Catcher:    http://127.0.0.1:8085"
echo "  MH Pattern:     http://127.0.0.1:8086"
echo "  Fear Trader:    http://127.0.0.1:8087"
echo ""
echo "👤 Login: freqtrader / freqtrade123"
echo ""
echo "📝 View Logs:"
echo "  tail -f /tmp/bot_8080.log  # Bollinger"
echo "  tail -f /tmp/bot_8081.log  # RSI-MACD"
echo "  tail -f /tmp/bot_8082.log  # Manual Control"
echo "  tail -f /tmp/bot_8083.log  # NFI X7"
echo "  tail -f /tmp/bot_8084.log  # E0V1E_v17"
echo "  tail -f /tmp/bot_8085.log  # Dip Catcher"
echo "  tail -f /tmp/bot_8086.log  # MH Pattern"
echo "  tail -f /tmp/bot_8087.log  # Fear Trader"
echo ""
echo "🛑 To stop all bots: ./stop_all_bots.sh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
