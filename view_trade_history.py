#!/Users/akshaykumar/freqtrade/.venv/bin/python3
"""
Trade History Viewer for Freqtrade Bots
Shows detailed buy/sell history with profit/loss for all bots
"""

import os
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth


# Configuration
BOTS = [
    {"name": "Bollinger Bands", "port": 8080, "emoji": "📊"},
    {"name": "RSI-MACD", "port": 8081, "emoji": "📈"},
    {"name": "Manual Control", "port": 8082, "emoji": "🎯"},
    {"name": "NFI X7", "port": 8083, "emoji": "♾️"},
    {"name": "E0V1E_v17", "port": 8084, "emoji": "🤖"},
    {"name": "Dip Catcher", "port": 8085, "emoji": "📉"},
    {"name": "MH Pattern", "port": 8086, "emoji": "🧠"},
    {"name": "Fear Trader", "port": 8087, "emoji": "😨"},
]
USERNAME = os.environ.get("FREQTRADE_USER", "freqtrader")
PASSWORD = os.environ.get("FREQTRADE_PASS", "freqtrade123")


def get_trades(port, limit=100):
    """Get trade history from a bot"""
    try:
        url = f"http://127.0.0.1:{port}/api/v1/trades"
        params = {"limit": limit}
        auth = HTTPBasicAuth(USERNAME, PASSWORD)
        response = requests.get(url, params=params, auth=auth, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return data.get("trades", [])
        return []
    except Exception as e:
        print(f"Error fetching trades from port {port}: {e}")
        return []


def format_date(date_str):
    """Format date string for display"""
    if not date_str or date_str == "Open":
        return "Open".ljust(19)
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return date_str[:19]


def display_trades(bot_name, emoji, trades):
    """Display trades for a bot"""
    print("\n" + "═" * 110)
    print(f"{emoji} {bot_name.upper()} - Trade History")
    print("═" * 110)

    if not trades:
        print("\n  No trades found.\n")
        return

    # Calculate statistics
    total_profit = 0
    winning_trades = 0
    losing_trades = 0
    total_fees = 0

    # Header
    cols = (
        f"{'ID':<5} {'Pair':<12} {'Entry Date':<19} {'Exit Date':<19} "
        f"{'Entry $':<12} {'Exit $':<12} {'Profit':<12} {'%':<8}"
    )
    print(f"\n{cols}")
    print("─" * 110)

    for trade in trades:
        trade_id = trade["trade_id"]
        pair = trade["pair"]
        open_date = format_date(trade.get("open_date", ""))
        close_date = format_date(trade.get("close_date", "Open"))

        open_rate = trade.get("open_rate", 0)
        close_rate = trade.get("close_rate", 0) if trade.get("close_rate") else 0

        profit_abs = trade.get("close_profit_abs", 0) if trade.get("close_profit_abs") else 0
        profit_pct = trade.get("profit_ratio", 0) * 100 if trade.get("profit_ratio") else 0

        # Track fees
        fee_open = trade.get("fee_open_cost", 0) or 0
        fee_close = trade.get("fee_close_cost", 0) or 0
        total_fees += fee_open + fee_close

        total_profit += profit_abs

        if profit_abs > 0:
            winning_trades += 1
            profit_indicator = "✅"
        elif profit_abs < 0:
            losing_trades += 1
            profit_indicator = "❌"
        else:
            profit_indicator = "⏸️"

        # Format values
        entry_str = f"${open_rate:,.2f}" if open_rate else "N/A"
        exit_str = f"${close_rate:,.2f}" if close_rate else "Open"
        profit_str = f"${profit_abs:.2f} {profit_indicator}"
        pct_str = f"{profit_pct:>6.2f}%"

        print(
            f"{trade_id:<5} {pair:<12} {open_date:<19} {close_date:<19} "
            f"{entry_str:<12} {exit_str:<12} {profit_str:<12} {pct_str:<8}"
        )

    # Summary
    print("─" * 110)
    total_trades = len(trades)
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

    print("\n📊 SUMMARY:")
    print(f"  Total Trades: {total_trades}")
    print(f"  Winning Trades: {winning_trades} ({win_rate:.1f}%)")
    print(f"  Losing Trades: {losing_trades}")
    print(f"  Total Fees Paid: ${total_fees:.2f}")

    if total_profit >= 0:
        print(f"  💰 Total Profit/Loss: ${total_profit:.2f} ✅")
    else:
        print(f"  💰 Total Profit/Loss: ${total_profit:.2f} ❌")

    print()


def display_combined_summary(all_trades_data):
    """Display combined summary across all bots"""
    print("\n" + "═" * 110)
    print("🌐 COMBINED SUMMARY - All Bots")
    print("═" * 110)

    total_trades = 0
    total_profit = 0
    total_wins = 0
    total_losses = 0
    total_fees = 0

    header = f"{'Bot':<25} {'Trades':<10} {'Wins':<10} {'Losses':<10} {'Win Rate':<12} {'P/L':<15}"
    print(f"\n{header}")
    print("─" * 110)

    for bot_name, trades in all_trades_data.items():
        if not trades:
            continue

        profit = sum(t.get("close_profit_abs", 0) or 0 for t in trades)
        wins = sum(1 for t in trades if (t.get("close_profit_abs", 0) or 0) > 0)
        losses = sum(1 for t in trades if (t.get("close_profit_abs", 0) or 0) < 0)
        fees = sum(
            (t.get("fee_open_cost", 0) or 0) + (t.get("fee_close_cost", 0) or 0) for t in trades
        )

        win_rate = (wins / len(trades) * 100) if len(trades) > 0 else 0

        profit_str = f"${profit:.2f} {'✅' if profit >= 0 else '❌'}"

        print(
            f"{bot_name:<25} {len(trades):<10} {wins:<10} {losses:<10} "
            f"{win_rate:>6.1f}%{'':<5} {profit_str:<15}"
        )

        total_trades += len(trades)
        total_profit += profit
        total_wins += wins
        total_losses += losses
        total_fees += fees

    print("─" * 110)
    overall_win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0
    overall_profit_str = f"${total_profit:.2f} {'✅' if total_profit >= 0 else '❌'}"

    footer = (
        f"{'TOTAL':<25} {total_trades:<10} {total_wins:<10} {total_losses:<10} "
        f"{overall_win_rate:>6.1f}%{'':<5} {overall_profit_str:<15}"
    )
    print(footer)
    print(f"\n💸 Total Fees Paid (All Bots): ${total_fees:.2f}")
    print(f"💰 Net Profit/Loss (All Bots): ${total_profit:.2f}")
    print()


def main():
    """Main function"""
    print("\n" + "═" * 110)
    print("📊 FREQTRADE TRADE HISTORY VIEWER")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 110)

    all_trades_data = {}

    # Fetch and display trades for each bot
    for bot in BOTS:
        trades = get_trades(bot["port"])
        all_trades_data[bot["name"]] = trades
        display_trades(bot["name"], bot["emoji"], trades)

    # Display combined summary
    if any(all_trades_data.values()):
        display_combined_summary(all_trades_data)
    else:
        print("\n⚠️  No trades found across all bots.\n")

    print("═" * 110)
    print("💡 Tip: Run this script anytime with: ./view_trade_history.py")
    print("═" * 110)
    print()


if __name__ == "__main__":
    main()
