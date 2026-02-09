#!/Users/akshaykumar/freqtrade/.venv/bin/python3
"""
Performance Optimized Live Price Display for Freqtrade Bots
Shows real-time current prices for all trading pairs across all bots
Displays both Spot and Futures prices for clarity on Bybit Testnet.
"""

import os
import time
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth


# Configuration
BOTS = [
    {"name": "Bollinger Bands", "port": 8080, "color": "\033[94m"},  # Blue
    {"name": "RSI-MACD", "port": 8081, "color": "\033[92m"},  # Green
    {"name": "Manual Control", "port": 8082, "color": "\033[93m"},  # Yellow
    {"name": "NFI X7", "port": 8083, "color": "\033[95m"},  # Magenta
    {"name": "E0V1E_v17", "port": 8084, "color": "\033[96m"},  # Cyan
    {"name": "Dip Catcher", "port": 8085, "color": "\033[91m"},  # Red
    {"name": "MH Pattern", "port": 8086, "color": "\033[97m"},  # White
    {"name": "Fear Trader", "port": 8087, "color": "\033[94m"},  # Blue
]
PAIRS_FUT = ["BTC/USDT:USDT", "ETH/USDT:USDT"]
PAIRS_SPOT = ["BTCUSDT", "ETHUSDT"]

USERNAME = os.environ.get("FREQTRADE_USER", "freqtrader")
PASSWORD = os.environ.get("FREQTRADE_PASS", "freqtrade123")
REFRESH_INTERVAL = 5
API_TIMEOUT = 5.0

# Color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"


def clear_screen():
    print("\033[H\033[J", end="")


def get_bybit_spot_price(symbol):
    """Fetch spot price directly from Bybit Public API"""
    try:
        url = f"https://api-testnet.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
        r = requests.get(url, timeout=3.0)
        if r.status_code == 200:
            data = r.json()
            if data.get("retCode") == 0 and data.get("result", {}).get("list"):
                return float(data["result"]["list"][0]["lastPrice"])
    except:
        pass
    return None


def get_prices(port, pairs):
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    prices = {}
    for pair in pairs:
        try:
            url = f"http://127.0.0.1:{port}/api/v1/pair_candles"
            params = {"pair": pair, "timeframe": "5m", "limit": 1}
            response = requests.get(url, params=params, auth=auth, timeout=2.0)
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    prices[pair] = float(data["data"][-1][4])
        except Exception:
            prices[pair] = None
    return prices


def get_bot_data(port):
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    data = {"status": "OFFLINE", "open_trades": 0, "balance": 0.0, "profit": 0.0}
    try:
        r_status = requests.get(f"http://127.0.0.1:{port}/api/v1/status", auth=auth, timeout=2.0)
        if r_status.status_code == 200:
            data["status"] = "ONLINE"
            data["open_trades"] = len(r_status.json())

        r_bal = requests.get(f"http://127.0.0.1:{port}/api/v1/balance", auth=auth, timeout=2.0)
        if r_bal.status_code == 200:
            bal_json = r_bal.json()
            for c in bal_json.get("currencies", []):
                if c.get("currency") == "USDT":
                    data["balance"] = c.get("balance", 0.0)
                    break

        r_profit = requests.get(f"http://127.0.0.1:{port}/api/v1/profit", auth=auth, timeout=2.0)
        if r_profit.status_code == 200:
            data["profit"] = r_profit.json().get("profit_all_ratio", 0.0) * 100
    except Exception:
        pass
    return data


def format_price(price):
    if price is None:
        return f"{RED}OFFLINE{RESET}"
    return f"${price:,.2f}"


def main():
    print(f"{BOLD}{CYAN}Starting Unified Price Monitor...{RESET}")
    while True:
        try:
            results = []
            prices_fut = {}

            # Fetch Spot directly for accuracy
            spot_btc = get_bybit_spot_price("BTCUSDT")
            spot_eth = get_bybit_spot_price("ETHUSDT")

            for bot in BOTS:
                data = get_bot_data(bot["port"])
                results.append(
                    {"name": bot["name"], "port": bot["port"], "color": bot["color"], "data": data}
                )
                if data["status"] == "ONLINE" and not prices_fut:
                    prices_fut = get_prices(bot["port"], PAIRS_FUT)

            clear_screen()
            print("═" * 80)
            print(f"{BOLD}📊 FREQTRADE CONSOLIDATED MONITOR (BYBIT TESTNET){RESET}".center(80))
            print(f"Updated: {datetime.now().strftime('%H:%M:%S')}".center(80))
            print("═" * 80)

            print(f"{BOLD}🌍 MARKET OVERVIEW{RESET}")
            print(
                f"  BTC/USDT: {BOLD}{CYAN}Spot: {format_price(spot_btc)}{RESET} | {BOLD}{MAGENTA}Futures: {format_price(prices_fut.get('BTC/USDT:USDT'))}{RESET}"
            )
            print(
                f"  ETH/USDT: {BOLD}{CYAN}Spot: {format_price(spot_eth)}{RESET} | {BOLD}{MAGENTA}Futures: {format_price(prices_fut.get('ETH/USDT:USDT'))}{RESET}"
            )
            print(
                "────────────────────────────────────────────────────────────────────────────────"
            )

            for info in results:
                d = info["data"]
                status = (
                    f"{GREEN}ONLINE{RESET}" if d["status"] == "ONLINE" else f"{RED}OFFLINE{RESET}"
                )
                header = (
                    f"🤖 {info['color']}{BOLD}{info['name']:<15}{RESET} [{info['port']}] - {status}"
                )
                if d["status"] == "ONLINE":
                    header += f" | {d['open_trades']} Trades | {d['balance']:>8,.2f} USDT | {d['profit']:>+6.2f}%"
                print(header)

            print("\n" + "═" * 80)
            print(f"{YELLOW}Note: Bybit Testnet Futures prices often diverge from Spot.{RESET}")
            print(f"Refreshing in {REFRESH_INTERVAL}s... Ctrl+C to stop")
            time.sleep(REFRESH_INTERVAL)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(REFRESH_INTERVAL)


if __name__ == "__main__":
    main()
