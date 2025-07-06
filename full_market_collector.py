import os
import sys
import time
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from dotenv import load_dotenv, find_dotenv

from src.utils.binance_data_provider import BinanceDataProvider
from src.utils.constants import Interval

load_dotenv(find_dotenv())

def get_all_symbols(client):
    info = client.get_exchange_info()
    return [s["symbol"] for s in info.get("symbols", []) if s.get("status") == "TRADING"]


def get_last_open_time(conn, symbol: str, interval: str):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT MAX(open_time) FROM price_data WHERE symbol=%s AND interval=%s",
            (symbol, interval),
        )
        row = cur.fetchone()
        return row[0] if row and row[0] else None


def collect_incremental(provider: BinanceDataProvider, symbol: str, interval: str):
    last_time = get_last_open_time(provider.conn, symbol, interval)
    if last_time:
        delta = Interval.from_string(interval).to_timedelta().to_pytimedelta()
        start_date = last_time + delta
    else:
        start_date = datetime(2017, 8, 17)
    try:
        provider.get_historical_klines(
            symbol,
            interval,
            start_date=start_date,
            end_date=datetime.utcnow(),
            use_cache=True,
        )
    except Exception as e:
        print(f"Failed to fetch {symbol} {interval}: {e}")


def main():
    provider = BinanceDataProvider()
    symbols = get_all_symbols(provider.client)
    intervals = [i.value for i in Interval]

    while True:
        for symbol in symbols:
            for interval in intervals:
                collect_incremental(provider, symbol, interval)
                time.sleep(0.2)
        time.sleep(60)


if __name__ == "__main__":
    main()
