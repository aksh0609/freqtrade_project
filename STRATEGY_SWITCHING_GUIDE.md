# 🚀 Freqtrade Strategy Switching Guide

## Quick Start Commands

### Check Bot Status
```bash
./check_status.sh
```

### Switch to RSI-MACD Strategy
```bash
./start_rsi_macd.sh
```

### Switch to Bollinger Bands Strategy
```bash
./start_bollinger.sh
```

### Stop the Bot
```bash
./stop_bot.sh
```

---

## 📊 Strategy Comparison

### RSI-MACD Strategy
**Type:** Trend Following
**Aggressiveness:** Conservative (fewer trades)
**Best For:** Strong trending markets

**Entry Conditions:**
- RSI drops below 30 (oversold)
- MACD crosses above signal line (bullish momentum)

**Exit Conditions:**
- RSI above 70 + MACD crosses below signal line
- OR 3% profit target
- OR -2% stop loss

**Performance (Dec 1-12):**
- Trades: 0 (very strict conditions)
- Waiting for significant price drops

---

### Bollinger Bands Strategy
**Type:** Mean Reversion
**Aggressiveness:** Active (~2 trades/day)
**Best For:** Ranging/sideways markets

**Entry Conditions:**
- Price touches lower Bollinger Band
- RSI below 35
- Sufficient volatility (BB width > 0.02)

**Exit Conditions:**
- Price returns to middle Bollinger Band
- OR RSI above 70
- OR 2.5% profit target
- OR -1.5% stop loss

**Performance (Dec 1-12):**
- Trades: 22
- Win Rate: 59.1%
- Average Duration: 41 minutes

---

## 💡 When to Use Which Strategy?

### Use RSI-MACD When:
- ✅ Market is trending strongly up or down
- ✅ You want fewer, potentially higher-quality trades
- ✅ You're patient and don't need frequent trades
- ✅ You expect significant price movements

### Use Bollinger Bands When:
- ✅ Market is moving sideways (ranging)
- ✅ You want more frequent trades
- ✅ You want to test and learn faster
- ✅ You prefer active trading with quick exits

---

## 🔄 How to Switch Strategies

### Method 1: Using Scripts (Easiest)

1. Open Terminal in freqtrade directory
2. Run the script for your desired strategy:
   ```bash
   ./start_rsi_macd.sh
   # OR
   ./start_bollinger.sh
   ```
3. The script will:
   - Stop the current bot
   - Start with the new strategy
   - Show confirmation message

### Method 2: Manual Command

```bash
# Stop current bot
pkill -f "freqtrade trade"

# Start with desired strategy
freqtrade trade -c user_data/config_bybit_spot.json --strategy RSI_MACD_Strategy
# OR
freqtrade trade -c user_data/config_bybit_spot.json --strategy BollingerBands_Strategy
```

---

## 📱 Monitoring After Switch

After switching strategies:

1. **Refresh Web UI** (http://127.0.0.1:7101)
2. **Check Dashboard** to see active strategy name
3. **View Logs** to confirm strategy loaded:
   ```bash
   tail -f user_data/logs/freqtrade.log
   ```

---

## ⚠️ Important Notes

### About Strategy Switching:
- **Cannot switch from UI** - This is a Freqtrade limitation
- **Requires bot restart** - Trades will be preserved
- **Open trades continue** - They follow the original strategy's exit rules
- **No data loss** - All trade history is saved in the database

### About Open Trades:
When you switch strategies:
- ✅ Open trades remain open
- ✅ They continue with their original entry strategy's exit rules
- ✅ New trades will use the new strategy
- ✅ Trade history is preserved

---

## 🎯 Recommended Workflow

### For Learning & Testing:
1. Start with **Bollinger Bands** (more trades to observe)
2. Run for 2-3 days
3. Analyze results in Web UI
4. Switch to **RSI-MACD** to compare
5. Choose your preferred strategy

### For Serious Trading:
1. Backtest both strategies over 30+ days
2. Compare win rates, profit, and drawdown
3. Choose based on current market conditions
4. Monitor and adjust as needed

---

## 📊 Performance Tracking

### Check Strategy Performance:
```bash
# View all trades
freqtrade trades-list -c user_data/config_bybit_spot.json

# View profit summary
freqtrade profit -c user_data/config_bybit_spot.json

# Backtest strategy
freqtrade backtesting -c user_data/config_bybit_spot.json --strategy [STRATEGY_NAME]
```

---

## 🆘 Troubleshooting

### Bot Won't Start:
```bash
# Check if another instance is running
ps aux | grep freqtrade

# Force stop all instances
pkill -9 -f "freqtrade trade"

# Try starting again
./start_rsi_macd.sh
```

### Web UI Not Loading:
```bash
# Check if bot is running
./check_status.sh

# Verify API is responding
curl http://127.0.0.1:7101/api/v1/ping
```

### Strategy Not Switching:
```bash
# Make sure old bot is stopped
./stop_bot.sh

# Wait a few seconds
sleep 3

# Start with new strategy
./start_bollinger.sh

# Verify strategy changed
./check_status.sh
```

---

## 📞 Support

- **Web UI:** http://127.0.0.1:7101
- **Freqtrade Docs:** https://www.freqtrade.io/en/stable/
- **Strategy Files:** `user_data/strategies/`
- **Config File:** `user_data/config_bybit_spot.json`

---

## 🎓 Next Steps

1. ✅ Try switching between both strategies
2. ✅ Monitor performance for each
3. ✅ Compare results in Web UI
4. ✅ Backtest with historical data
5. ✅ Choose your preferred strategy
6. ✅ Consider creating your own custom strategy!

Happy Trading! 🚀
