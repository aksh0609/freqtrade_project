import os
import sys

import requests


# --- Configuration ---
BOTS = [
    {"name": "Bollinger Bands", "port": 8080, "color": "\033[94m"},  # Blue
    {"name": "RSI-MACD", "port": 8081, "color": "\033[92m"},  # Green
    {"name": "Manual Scalper", "port": 8082, "color": "\033[93m"},  # Yellow
]
USERNAME = os.environ.get("FREQTRADE_USER", "freqtrader")
PASSWORD = os.environ.get("FREQTRADE_PASS", "freqtrade123")

# --- Colors ---
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
CYAN = "\033[96m"


class FreqtradeClient:
    def __init__(self, bot_config):
        self.name = bot_config["name"]
        self.port = bot_config["port"]
        self.color = bot_config["color"]
        self.base_url = f"http://127.0.0.1:{self.port}/api/v1"
        self.access_token = None

    def login(self):
        """Authenticates and gets an access token."""
        try:
            response = requests.post(
                f"{self.base_url}/token/login",
                auth=(USERNAME, PASSWORD),
                timeout=2,
            )
            if response.status_code == 200:
                self.access_token = response.json().get("access_token")
                return True
            else:
                print(
                    f"{RED}[!] {self.name} (Port {self.port}): "
                    f"Login Failed - {response.status_code}{RESET}"
                )
                return False
        except requests.exceptions.RequestException:
            print(
                f"{RED}[!] {self.name} (Port {self.port}): "
                f"Connection Refused (Is it running?){RESET}"
            )
            return False

    def _headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_status(self):
        if not self.access_token:
            return None
        try:
            # Get trade count
            trades_data = requests.get(
                f"{self.base_url}/status", headers=self._headers(), timeout=2
            ).json()

            if isinstance(trades_data, list):
                count = len(trades_data)
            else:
                count = len(trades_data.get("trades", []))

            # Get profit
            profit = requests.get(
                f"{self.base_url}/profit", headers=self._headers(), timeout=2
            ).json()
            return {
                "running": True,
                "trade_count": count,
                "profit_pct": profit.get("profit_all_percent", 0.0),
            }
        except Exception:
            return None

    def get_balance(self):
        if not self.access_token:
            return {}
        try:
            return requests.get(
                f"{self.base_url}/balance", headers=self._headers(), timeout=2
            ).json()
        except Exception:
            return {}

    def force_entry(self, pair, price=None):
        if not self.access_token:
            return False
        payload = {"pair": pair}
        if price:
            payload["price"] = price

        try:
            res = requests.post(
                f"{self.base_url}/forceenter",
                json=payload,
                headers=self._headers(),
                timeout=10,
            )
            return res.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_open_trades(self):
        if not self.access_token:
            return []
        try:
            res = requests.get(f"{self.base_url}/status", headers=self._headers(), timeout=10)
            data = res.json()
            if isinstance(data, list):
                return data
            return data.get("trades", [])
        except Exception:
            return []

    def force_exit(self, trade_id):
        if not self.access_token:
            return False
        try:
            res = requests.post(
                f"{self.base_url}/forceexit",
                json={"trade_id": trade_id},
                headers=self._headers(),
                timeout=10,
            )
            return res.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}


# --- UI Functions ---


def clear_screen():
    print("\033[H\033[J", end="")


def print_header():
    clear_screen()
    print(f"{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BOLD} 🕹️  FREQTRADE MANUAL CONTROL PANEL{RESET}")
    print(f"{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print("")


def show_dashboard(clients):
    print_header()
    print(f"{BOLD}STATUS OVERVIEW:{RESET}")
    for client in clients:
        status = client.get_status()
        status_str = f"{RED}OFFLINE{RESET}"
        details = ""
        if status:
            status_str = f"\033[92mONLINE{RESET}"
            details = (
                f"| Open Trades: {status['trade_count']} | Profit: {status['profit_pct']:.2f}%"
            )

        print(
            f"  {client.color}● {client.name:<20}{RESET} [{client.port}] : {status_str} {details}"
        )
    print("")


def select_bot(clients):
    print(f"{BOLD}SELECT A BOT TO CONTROL:{RESET}")
    for i, client in enumerate(clients):
        print(f"  {i + 1}. {client.name} ({client.port})")
    print("  0. Cancel")

    try:
        choice_input = input(f"\n{CYAN}Choice > {RESET}")
        choice = int(choice_input) if choice_input.isdigit() else 0
        if 0 < choice <= len(clients):
            return clients[choice - 1]
        return None
    except Exception:
        return None


def wrapper_buy(client):
    print(f"\n{BOLD}💰 BUY (Force Entry) - {client.name}{RESET}")
    pair = input("Enter Pair (e.g. BTC/USDT) > ").strip().upper()
    if not pair:
        return

    print(f"Attempting to buy {pair}...")
    result = client.force_entry(pair)
    print(f"\nResult: {result}")
    input("\nPress Enter to continue...")


def wrapper_sell(client):
    print(f"\n{BOLD}🛑 SELL (Force Exit) - {client.name}{RESET}")
    trades = client.get_open_trades()

    if not trades:
        print("No open trades found.")
        input("\nPress Enter to continue...")
        return

    print("Open Trades:")
    for i, t in enumerate(trades):
        print(
            f"  {i + 1}. Trade ID: {t['trade_id']} | Pair: {t['pair']} | "
            f"Profit: {t['profit_ratio']:.2%}"
        )

    try:
        choice_input = input("\nSelect trade to sell (0 to cancel) > ")
        choice = int(choice_input) if choice_input.isdigit() else 0
        if 0 < choice <= len(trades):
            trade_id = trades[choice - 1]["trade_id"]
            result = client.force_exit(trade_id)
            print(f"\nResult: {result}")
    except Exception:  # noqa: S110
        pass
    input("\nPress Enter to continue...")


def main():
    clients = []
    print("Connecting to bots...")
    for b in BOTS:
        c = FreqtradeClient(b)
        c.login()
        clients.append(c)

    while True:
        show_dashboard(clients)

        print(f"{BOLD}MAIN MENU:{RESET}")
        print("  1. 💰 Manual BUY (Force Entry)")
        print("  2. 🛑 Manual SELL (Force Exit)")
        print("  3. 🔄 Refresh Status")
        print("  4. 🚪 Quit")

        choice = input(f"\n{CYAN}Option > {RESET}")

        if choice == "1":
            bot = select_bot(clients)
            if bot:
                wrapper_buy(bot)
        elif choice == "2":
            bot = select_bot(clients)
            if bot:
                wrapper_sell(bot)
        elif choice == "3":
            # Re-login to refresh tokens/check status
            print("Refreshing...")
            for c in clients:
                c.login()
            pass
        elif choice == "4":
            print("Exiting.")
            sys.exit(0)
        else:
            pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
