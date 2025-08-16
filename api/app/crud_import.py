import sqlite3
import pandas as pd
import os

DB_PATH = "./data/surgicalops.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn

def import_all(db_path: str, data_dir: str) -> dict:
    """
    Import all Excel files (products, clients, client pricing, stock)
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # --- CREATE TABLES IF NOT EXISTS ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        code TEXT PRIMARY KEY,
        description TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id TEXT PRIMARY KEY,
        name TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client_pricing (
        client_id TEXT,
        code TEXT,
        price REAL,
        PRIMARY KEY(client_id, code)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock_ledger (
        box_id TEXT,
        code TEXT,
        qty INTEGER,
        PRIMARY KEY(box_id, code)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock_movements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        box_id TEXT,
        qty INTEGER,
        ref_type TEXT,
        ref_id TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()

    # --- IMPORT PRODUCTS ---
    products_file = os.path.join(data_dir, "products.xlsx")
    df = pd.read_excel(products_file)
    for _, row in df.iterrows():
        cur.execute("INSERT OR REPLACE INTO products (code, description) VALUES (?, ?)",
                    (row['code'], row['description']))

    # --- IMPORT CLIENTS ---
    clients_file = os.path.join(data_dir, "clients.xlsx")
    df = pd.read_excel(clients_file)
    for _, row in df.iterrows():
        cur.execute("INSERT OR REPLACE INTO clients (client_id, name) VALUES (?, ?)",
                    (row['client_id'], row['client_name']))

    # --- IMPORT CLIENT PRICING ---
    pricing_file = os.path.join(data_dir, "client_pricing.xlsx")
    df = pd.read_excel(pricing_file)
    for _, row in df.iterrows():
        cur.execute("INSERT OR REPLACE INTO client_pricing (client_id, code, price) VALUES (?, ?, ?)",
                    (row['client_id'], row['code'], row['price']))

    # --- IMPORT STOCK LEDGER ---
    stock_file = os.path.join(data_dir, "opening_stock.xlsx")
    df = pd.read_excel(stock_file)
    for _, row in df.iterrows():
        cur.execute("INSERT OR REPLACE INTO stock_ledger (box_id, code, qty) VALUES (?, ?, ?)",
                    (row['box_id'], row['code'], row['qty']))

    conn.commit()
    conn.close()

    return {
        "products": len(pd.read_excel(products_file)),
        "clients": len(pd.read_excel(clients_file)),
        "client_pricing": len(pd.read_excel(pricing_file)),
        "stock": len(pd.read_excel(stock_file))
    }
