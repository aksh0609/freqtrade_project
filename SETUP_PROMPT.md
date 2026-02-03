# 🚀 Freqtrade Multi-Bot Project Setup Guide

This document provides a complete "Prompt" and step-by-step instructions to recreate this specific multi-bot trading environment on a new computer.

## 📋 Project Overview

This project is a highly customized **Freqtrade** setup running 6 simultaneous strategies on Bybit Testnet. It includes a custom unified monitoring Python script and a web-based "Commander" dashboard.

### Active Strategies & Ports

1. **Bollinger Bands**: Port 8080
2. **RSI-MACD**: Port 8081
3. **Manual Scalper**: Port 8082
4. **NFI X7**: Port 8083
5. **E0V1E_v17**: Port 8084
6. **Dip Catcher**: Port 8085
7. **Commander Web UI**: Port 8000

---

## 🛠️ Step 1: Prerequisites

Ensure the new computer has:

* **Python 3.10+**
* **Git** installed.
* **Docker Desktop** (Required for Method B, recommended for stability).
* **System Tools**:
  * *Mac:* `xcode-select --install`
  * *Linux:* `sudo apt update && sudo apt install -y python3-pip python3-venv libssl-dev`

---

## 📦 Step 2: Migration (Method A - Manual Local Setup)

### 1. Transfer Files

Copy the entire `freqtrade` directory to the new computer.
**Important:** Ensure these are included:
* `user_data/` (Strategies, Configs, and `.sqlite` databases).
* `live_price_display.py` and `fetch_ticker.py`.
* `start_all_bots.sh` and `stop_all_bots.sh`.
* `web_dashboard/` directory.

### 2. Initialize Environment

In the new project directory:

```bash
# Delete old venv if it exists
rm -rf .venv

# Run setup script or manual install
./setup.sh --install

# Install specific dependencies
./.venv/bin/pip install requests ccxt
```

### 3. Update Paths

Search for absolute paths (e.g., `/Users/akshaykumar/freqtrade`) in the following files and update them to your new directory location:
* `start_all_bots.sh`
* `start_commander.sh`
* `live_price_display.py`

---

## 🐳 Step 3: Migration (Method B - Docker Setup)

This is the most stable method for moving to a different OS.

1. **Move Files**: Copy your `user_data/` folder and `docker-compose.yml` to the new machine.
2. **Launch**:

   ```bash
   docker-compose pull
   docker-compose up -d
   ```

3. **Status**: Monitor logs with `docker-compose logs -f`.

---

## 🚀 Step 4: Launch & Monitor

### Start All Bots

```bash
./start_all_bots.sh
```

### Start Live Terminal Monitor

```bash
./.venv/bin/python3 live_price_display.py
```

### Start Web Commander

```bash
./start_commander.sh
# Then open http://127.0.0.1:8000 in your browser
```

---

## 🤖 Instructions for AI Assistants

If you are an AI agent helping to set up this project:

1. **Verify Files**: Check that all 6 config files exist in `user_data/`.
2. **Path Correction**: Automatically update shebangs and absolute paths in `.sh` files to match the current working directory.
3. **API Integrity**: Check `user_data/config_*.json` for API keys and ensure they match the exchange requirements.
4. **Database Migration**: Ensure `.sqlite` files are present in `user_data/` to preserve historical profit data.
5. **Connectivity**: Test API connectivity with `python3 test_bybit.py` before starting all bots.

---
**Author:** Antigravity AI
**Date:** 2026-02-02
