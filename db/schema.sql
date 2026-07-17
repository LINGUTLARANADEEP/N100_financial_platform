CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    company_name TEXT,
    website TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

CREATE TABLE profitandloss (
    company_id TEXT,
    year INTEGER
);

CREATE TABLE balancesheet (
    company_id TEXT,
    year INTEGER
);

CREATE TABLE cashflow (
    company_id TEXT,
    year INTEGER
);

CREATE TABLE analysis (
    company_id TEXT
);

CREATE TABLE documents (
    company_id TEXT
);

CREATE TABLE financial_ratios (
    company_id TEXT
);

CREATE TABLE market_cap (
    company_id TEXT
);

CREATE TABLE peer_groups (
    company_id TEXT
);

CREATE TABLE prosandcons (
    company_id TEXT
);

CREATE TABLE sectors (
    company_id TEXT
);

CREATE TABLE stock_prices (
    company_id TEXT
);