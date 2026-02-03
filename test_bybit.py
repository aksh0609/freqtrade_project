import sys

import ccxt


key = "hXXppKblo10gZWwkus"
secret = "SBwGh2lWWB3mz5H2m6QNTk4aMhx9YveWHVFh"  # noqa: S105

print(f"Testing Key: {key}")
print(f"Testing Secret: {secret[:5]}...{secret[-5:]}")

exchange = ccxt.bybit(
    {"apiKey": key, "secret": secret, "enableRateLimit": True, "options": {"defaultType": "spot"}}
)
exchange.set_sandbox_mode(True)

try:
    print("1. Testing Public API (fetch_time)...")
    server_time = exchange.fetch_time()
    print(f"✅ Public API works. Server time: {server_time}")
except Exception as e:
    print(f"❌ Public API failed: {e}")
    sys.exit(1)

try:
    print("2. Testing Private API (Balances)...")
    for acc_type in ["spot", "funding", "unified"]:
        try:
            bal = exchange.fetch_balance({"type": acc_type})
            usdt = bal.get("USDT", {}).get("total", 0)
            print(f"💰 {acc_type.capitalize()} USDT: {usdt}")
        except Exception as e:
            print(f"⚠️  Could not fetch {acc_type} balance: {str(e)[:50]}...")

    # Default balance (what the bot sees)
    bal = exchange.fetch_balance()
    usdt = bal.get("USDT", {}).get("free", 0)
    print(f"\n🤖 Freqtrade (Default) sees: {usdt} USDT")

    if usdt == 0:
        print("\n⚠️  CRITICAL: The bot CANNOT see your Funding account funds.")
        print("   You must transfer them to 'Spot' or 'Unified' on the Bybit website.")
except Exception as e:
    print(f"❌ Private API failed (Authentication Error): {e}")
    if "10003" in str(e):
        print(
            "💡 Hint: error 10003 means the key is invalid. Double check typos or Bybit propagation."  # noqa: E501
        )
    elif "10005" in str(e):
        print("💡 Hint: error 10005 means your IP is not whitelisted on Bybit.")
    sys.exit(1)
