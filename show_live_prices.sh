#!/bin/bash

# Live Price Monitor for All Bots
# Shows current prices for BTC/USDT and ETH/USDT from all three bots

PYTHON_ENV=".venv/bin/python3"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 LIVE PRICE MONITOR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Fetching prices using CCXT..."
echo "Press Ctrl+C to stop"
echo ""

while true; do
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 LIVE PRICES - Updated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🔍 Fetching market data... (please wait)"
    
    # Fetch all prices in one go for efficiency
    MAINNET_DATA=$($PYTHON_ENV fetch_ticker.py bybit false BTC/USDT ETH/USDT)
    SANDBOX_DATA=$($PYTHON_ENV fetch_ticker.py bybit true BTC/USDT ETH/USDT)

    # Redraw screen with data
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 LIVE PRICES - Updated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    echo "🌍 MAINNET PRICES (Actual Market):"
    echo "$MAINNET_DATA" | sed 's/^/  /'
    echo ""

    echo "🧪 SANDBOX PRICES (Testnet - Bots Use This):"
    echo "$SANDBOX_DATA" | sed 's/^/  /'
    echo ""

    echo "🤖 Bot Status:"
    # Check if bots are running using more robust ps grep
    if ps aux | grep -v grep | grep "config_bollinger_8080" > /dev/null; then echo "  Bot 1 (Bollinger): [Running] - http://127.0.0.1:7101"; else echo "  Bot 1 (Bollinger): [\033[91mStopped\033[0m] - http://127.0.0.1:7101"; fi
    if ps aux | grep -v grep | grep "config_rsi_macd_8081" > /dev/null; then echo "  Bot 2 (RSI-MACD):  [Running] - http://127.0.0.1:7102"; else echo "  Bot 2 (RSI-MACD):  [\033[91mStopped\033[0m] - http://127.0.0.1:7102"; fi
    if ps aux | grep -v grep | grep "config_scalper_8082" > /dev/null; then echo "  Bot 3 (Manual):    [Running] - http://127.0.0.1:7103"; else echo "  Bot 3 (Manual):    [\033[91mStopped\033[0m] - http://127.0.0.1:7103"; fi
    if ps aux | grep -v grep | grep "config_nfi_8083" > /dev/null; then echo "  Bot 4 (NFI X7):    [Running] - http://127.0.0.1:7104"; else echo "  Bot 4 (NFI X7):    [\033[91mStopped\033[0m] - http://127.0.0.1:7104"; fi
    if ps aux | grep -v grep | grep "config_e0v1e_8084" > /dev/null; then echo "  Bot 5 (E0V1E):     [Running] - http://127.0.0.1:7105"; else echo "  Bot 5 (E0V1E):     [\033[91mStopped\033[0m] - http://127.0.0.1:7105"; fi
    if ps aux | grep -v grep | grep "config_dip_catcher_8085" > /dev/null; then echo "  Bot 6 (Dip Catch): [Running] - http://127.0.0.1:7106"; else echo "  Bot 6 (Dip Catch): [\033[91mStopped\033[0m] - http://127.0.0.1:7106"; fi
    if ps aux | grep -v grep | grep "config_mh_8086" > /dev/null; then echo "  Bot 7 (MH Patt):   [Running] - http://127.0.0.1:7107"; else echo "  Bot 7 (MH Patt):   [\033[91mStopped\033[0m] - http://127.0.0.1:7107"; fi
    if ps aux | grep -v grep | grep "config_fear_8087" > /dev/null; then echo "  Bot 8 (Fear Trd):  [Running] - http://127.0.0.1:7108"; else echo "  Bot 8 (Fear Trd):  [\033[91mStopped\033[0m] - http://127.0.0.1:7108"; fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Refreshing in 5 seconds... (Ctrl+C to stop)"
    echo "Bots not running? Start them with: ./start_all_bots.sh"
    echo ""

    sleep 5
done
