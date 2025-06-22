-- SQL initialization script for the trading database

-- Table: accounts
CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY,
    owner TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cash_balance REAL NOT NULL DEFAULT 0,
    margin_requirement REAL NOT NULL DEFAULT 0,
    margin_used REAL NOT NULL DEFAULT 0,
    last_update TIMESTAMP
);

-- Table: trades
CREATE TABLE IF NOT EXISTS trades (
    trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    side TEXT NOT NULL,
    quantity REAL NOT NULL,
    price REAL NOT NULL,
    fee REAL DEFAULT 0,
    realized_pl REAL DEFAULT 0,
    strategy_name TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- Table: positions
CREATE TABLE IF NOT EXISTS positions (
    position_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    long_qty REAL DEFAULT 0,
    short_qty REAL DEFAULT 0,
    long_cost_basis REAL DEFAULT 0,
    short_cost_basis REAL DEFAULT 0,
    short_margin_used REAL DEFAULT 0,
    opened_at TIMESTAMP NOT NULL,
    closed_at TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- Table: price_data
CREATE TABLE IF NOT EXISTS price_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    open_time TIMESTAMP NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume REAL NOT NULL,
    close_time TIMESTAMP NOT NULL,
    quote_volume REAL,
    count INTEGER,
    taker_buy_volume REAL,
    taker_buy_quote_volume REAL
);

-- Table: strategy_signals
CREATE TABLE IF NOT EXISTS strategy_signals (
    signal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    strategy_name TEXT NOT NULL,
    signal TEXT NOT NULL,
    confidence REAL,
    metrics TEXT
);

-- Table: portfolio_history
CREATE TABLE IF NOT EXISTS portfolio_history (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    portfolio_value REAL NOT NULL,
    long_exposure REAL,
    short_exposure REAL,
    gross_exposure REAL,
    net_exposure REAL,
    long_short_ratio REAL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
