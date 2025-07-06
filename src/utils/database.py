"""Simple PostgreSQL helper utilities."""

import os
from pathlib import Path
from typing import Iterable
from dotenv import load_dotenv, find_dotenv

import psycopg2
from psycopg2.extras import RealDictCursor, execute_batch

load_dotenv(find_dotenv())


SCHEMA_PATH = Path("init.sql")

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "trading")

DEFAULT_DSN = os.getenv(
    "DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)


def init_db(conn, schema_path: Path = SCHEMA_PATH) -> None:
    """Create tables if they do not exist."""
    with conn.cursor() as cur, open(schema_path, "r") as f:
        cur.execute(f.read())
    conn.commit()


def get_connection(dsn: str = DEFAULT_DSN):
    """Return a PostgreSQL connection and ensure schema exists."""
    conn = psycopg2.connect(dsn, cursor_factory=RealDictCursor)
    init_db(conn)
    return conn


def _records_from_df(df, symbol: str, interval: str) -> Iterable[tuple]:
    cols = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_volume",
        "count",
        "taker_buy_volume",
        "taker_buy_quote_volume",
    ]
    df_slice = df[cols].copy()
    df_slice["symbol"] = symbol
    df_slice["interval"] = interval
    return [tuple(row) for row in df_slice.to_records(index=False)]


def insert_price_data(df, symbol: str, interval: str, conn) -> None:
    """Save price data DataFrame to the database."""
    if df.empty:
        return

    records = _records_from_df(df, symbol, interval)
    columns = (
        "open_time, open, high, low, close, volume, close_time, quote_volume, count,"
        " taker_buy_volume, taker_buy_quote_volume, symbol, interval"
    )
    query = f"INSERT INTO price_data ({columns}) VALUES (" + ",".join(["%s"] * 13) + ")"
    with conn.cursor() as cur:
        execute_batch(cur, query, records)
    conn.commit()
