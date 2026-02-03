# 🤖 Multiple Bots Setup Guide

## Overview

You can now run **multiple Freqtrade bots simultaneously**, each with:
- ✅ Different strategy
- ✅ Different port number
- ✅ Different Web UI
- ✅ Separate database
- ✅ Independent configuration

---

## 📊 Bot Configuration

### Bot 1: Bollinger Bands Strategy
- **Port:** 8080
- **Web UI:** http://127.0.0.1:8080
- **Strategy:** BollingerBands_Strategy
- **Config:** [config_bollinger_8080.json](user_data/config_bollinger_8080.json)
- **Database:** tradesv3.bollinger.dryrun.sqlite
- **Wallet:** 333 USDT (33% of 1000)

### Bot 2: RSI-MACD Strategy
- **Port:** 8081
- **Web UI:** http://127.0.0.1:8081
- **Strategy:** RSI_MACD_Strategy
- **Config:** [config_rsi_macd_8081.json](user_data/config_rsi_macd_8081.json)
- **Database:** tradesv3.rsi_macd.dryrun.sqlite
- **Wallet:** 333 USDT (33% of 1000)

### Bot 3: Scalper Strategy (Reserved)
- **Port:** 8082
- **Web UI:** http://127.0.0.1:8082
- **Strategy:** Scalper_Strategy (to be created)
- **Config:** [config_scalper_8082.json](user_data/config_scalper_8082.json)
- **Database:** tradesv3.scalper.dryrun.sqlite
- **Wallet:** 334 USDT (34% of 1000)

---

## 🚀 Quick Start Commands

### Start All Bots
```bash
./start_all_bots.sh
```
This starts all configured bots simultaneously

### Check Bot Status
```bash
./check_all_bots.sh
```
Shows which bots are running and their status

### Stop All Bots
```bash
./stop_all_bots.sh
```
Stops all running bots gracefully

---

## 🎯 Start Individual Bots

### Option 1: Start One Bot at a Time
```bash
# Bollinger Bands Bot
freqtrade trade -c user_data/config_bollinger_8080.json --strategy BollingerBands_Strategy &

# RSI-MACD Bot
freqtrade trade -c user_data/config_rsi_macd_8081.json --strategy RSI_MACD_Strategy &

# Scalper Bot (when strategy is created)
freqtrade trade -c user_data/config_scalper_8082.json --strategy Scalper_Strategy &
```

### Option 2: Use Start Script
```bash
./start_all_bots.sh
```

---

## 🌐 Access Web UIs

Once bots are running, access each Web UI:

| Bot | URL | Login |
|-----|-----|-------|
| **Bollinger Bands** | http://127.0.0.1:8080 | freqtrader / freqtrade123 |
| **RSI-MACD** | http://127.0.0.1:8081 | freqtrader / freqtrade123 |
| **Scalper** | http://127.0.0.1:8082 | freqtrader / freqtrade123 |

**Pro Tip:** Open each URL in a different browser tab to monitor all bots simultaneously!

---

## 📊 Monitor Multiple Bots

### View All Bot Logs
```bash
# Bollinger Bands logs
tail -f /tmp/bot_8080.log

# RSI-MACD logs
tail -f /tmp/bot_8081.log

# Scalper logs
tail -f /tmp/bot_8082.log

# View all simultaneously (split terminal)
tail -f /tmp/bot_8080.log /tmp/bot_8081.log
```

### Check API Status
```bash
# Quick ping test
curl http://127.0.0.1:8080/api/v1/ping  # Bollinger
curl http://127.0.0.1:8081/api/v1/ping  # RSI-MACD
curl http://127.0.0.1:8082/api/v1/ping  # Scalper
```

### View All Trades
```bash
# Bollinger Bands trades
freqtrade trades-list --db-url sqlite:///tradesv3.bollinger.dryrun.sqlite

# RSI-MACD trades
freqtrade trades-list --db-url sqlite:///tradesv3.rsi_macd.dryrun.sqlite

# Scalper trades
freqtrade trades-list --db-url sqlite:///tradesv3.scalper.dryrun.sqlite
```

---

## ⚙️ Important Configuration Notes

### 1. **Separate Databases**
Each bot uses its own database to avoid conflicts:
- `tradesv3.bollinger.dryrun.sqlite`
- `tradesv3.rsi_macd.dryrun.sqlite`
- `tradesv3.scalper.dryrun.sqlite`

### 2. **Wallet Division**
Total 1000 USDT dry-run wallet is divided:
- 33% (333 USDT) → Bollinger Bands
- 33% (333 USDT) → RSI-MACD
- 34% (334 USDT) → Scalper

This prevents over-allocation of funds!

### 3. **Different JWT Tokens**
Each bot has unique security tokens to prevent session conflicts.

### 4. **Same API Keys**
All bots share the same Bybit API keys (safe for dry-run).

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Check what's using port 8080
lsof -i :8080

# Kill process on port
kill -9 $(lsof -t -i:8080)
```

### Bot Won't Start
```bash
# Check if another bot is using the same database
ps aux | grep freqtrade

# Stop all bots and try again
./stop_all_bots.sh
sleep 3
./start_all_bots.sh
```

### Web UI Not Loading
```bash
# Verify bot is running
./check_all_bots.sh

# Check logs for errors
tail -50 /tmp/bot_8080.log
```

---

## 📈 Performance Comparison

With multiple bots running, you can:

### Compare Strategies Live
- Open all 3 Web UIs side by side
- Compare which strategy performs best
- Analyze different entry/exit points

### Diversify Risk
- Different strategies reduce overall risk
- One strategy might catch opportunities others miss
- Better overall portfolio performance

### Independent Operation
- Each bot operates completely independently
- No conflicts between strategies
- Separate P&L tracking

---

## 💡 Best Practices

### 1. **Monitor Resource Usage**
Running 3 bots simultaneously uses more CPU/RAM:
```bash
# Check system resources
top | grep freqtrade
```

### 2. **Stagger Bot Starts**
Start bots with a few seconds delay:
```bash
./start_all_bots.sh  # Already handles delays
```

### 3. **Use Screen/Tmux for Long-Term**
For running bots 24/7:
```bash
# Start in screen session
screen -S freqtrade_bots
./start_all_bots.sh
# Detach: Ctrl+A, D
# Reattach: screen -r freqtrade_bots
```

### 4. **Regular Backups**
Backup all databases regularly:
```bash
cp tradesv3.*.sqlite backups/
```

---

## 🎯 Adding More Bots

To add Bot 4, 5, etc.:

1. **Create new config file:**
   - Copy existing config
   - Change `listen_port` to 8083, 8084, etc.
   - Change `bot_name`
   - Change `db_url`

2. **Update start script:**
   - Add new bot launch command
   - Add to start_all_bots.sh

3. **Allocate wallet:**
   - Divide dry_run_wallet appropriately
   - Update tradable_balance_ratio

---

## 📞 Summary

**You now have:**
✅ 3 separate bot configurations
✅ 3 different Web UIs (ports 8080, 8081, 8082)
✅ Scripts to start/stop/check all bots
✅ Separate databases for each strategy
✅ Wallet division across all bots

**Ready to use!** Just run `./start_all_bots.sh` to begin! 🚀

---

## 🆘 Need Help?

```bash
# Check bot status
./check_all_bots.sh

# View logs
tail -f /tmp/bot_8080.log

# Stop everything
./stop_all_bots.sh
```
