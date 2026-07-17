import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DB_PATH = ROOT / "db" / "nifty100.db"

print("Database path:", DB_PATH)
print("Exists:", DB_PATH.exists())


@st.cache_data(ttl=600)
def run_query(query, params=None):
    conn = sqlite3.connect(DB_PATH)

    if params:
        df = pd.read_sql(query, conn, params=params)
    else:
        df = pd.read_sql(query, conn)

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_companies():
    return run_query("""
        SELECT DISTINCT
            company_id
        FROM financial_ratios
        ORDER BY company_id
    """)


@st.cache_data(ttl=600)
def get_ratios(company_id, year=None):

    if year:
        return run_query("""
            SELECT *
            FROM financial_ratios
            WHERE company_id=?
            AND year=?
        """, (company_id, year))

    return run_query("""
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
    """, (company_id,))


@st.cache_data(ttl=600)
def get_pl(company_id):

    return run_query("""
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
    """, (company_id,))


@st.cache_data(ttl=600)
def get_bs(company_id):

    return run_query("""
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
    """, (company_id,))


@st.cache_data(ttl=600)
def get_cf(company_id):

    return run_query("""
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
    """, (company_id,))


@st.cache_data(ttl=600)
def get_sectors():

    return run_query("""
        SELECT *
        FROM sectors
        ORDER BY broad_sector
    """)


@st.cache_data(ttl=600)
def get_peers(sector):

    return run_query("""
        SELECT *
        FROM financial_ratios fr
        JOIN sectors s
        ON fr.company_id=s.company_id
        WHERE s.broad_sector=?
    """, (sector,))


@st.cache_data(ttl=600)
def get_valuation(company_id):

    return run_query("""
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year DESC
        LIMIT 1
    """, (company_id,))