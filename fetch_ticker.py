import sys
import ccxt
import time


def get_ticker_prices(exchange_name, pairs, sandbox=False):
    """
    Fetches the last traded prices for multiple pairs on a specified exchange.
    Returns a dictionary of pair -> price.
    """
    results = {}
    try:
        exchange_class = getattr(ccxt, exchange_name)
        exchange = exchange_class({"enableRateLimit": True, "timeout": 5000})
        if sandbox:
            exchange.set_sandbox_mode(True)

        # Try to fetch all at once if possible (some exchanges support this)
        try:
            tickers = exchange.fetch_tickers(pairs)
            for pair in pairs:
                if pair in tickers and "last" in tickers[pair]:
                    results[pair] = tickers[pair]["last"]
                else:
                    results[pair] = None
        except Exception:
            # Fallback to sequential if fetch_tickers fails
            for pair in pairs:
                try:
                    ticker = exchange.fetch_ticker(pair)
                    results[pair] = ticker["last"]
                except Exception:
                    results[pair] = None

    except Exception:
        for pair in pairs:
            results[pair] = None

    return results


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 fetch_ticker.py <exchange> <sandbox:true|false> <pair1> [pair2] ...")
        sys.exit(1)

    exchange_name = sys.argv[1]
    use_sandbox = sys.argv[2].lower() == "true"
    pairs = sys.argv[3:]

    start_time = time.time()
    prices = get_ticker_prices(exchange_name, pairs, use_sandbox)

    for pair in pairs:
        price = prices.get(pair)
        if price is not None:
            print(f"{pair}: ${price:,.2f}")
        else:
            print(f"{pair}: N/A")
