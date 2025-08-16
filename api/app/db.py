import sqlite3
from typing import List, Dict

DB_PATH = "./data/surgicalops.db"

# --- UTILITY FUNCTIONS ---

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- STOCK FUNCTIONS ---

def get_available_stock(code: str) -> List[Dict]:
    """
    Returns list of boxes with available quantity for a given product code
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT box_id, qty FROM stock_ledger WHERE code=? AND qty>0", (code,))
    rows = cur.fetchall()
    conn.close()
    return [{"box_id": r["box_id"], "qty": r["qty"]} for r in rows]

def pick_stock(code: str, picks: List[Dict], ref_type: str, ref_id: str) -> Dict:
    """
    Deduct quantity from inventory when confirmed
    picks = [{"box_id": "B-001", "qty": 10}]
    """
    conn = get_conn()
    cur = conn.cursor()
    for pick in picks:
        box_id = pick["box_id"]
        qty = pick["qty"]
        # check available
        cur.execute("SELECT qty FROM stock_ledger WHERE code=? AND box_id=?", (code, box_id))
        row = cur.fetchone()
        if not row:
            conn.close()
            raise Exception(f"No stock found for {code} in box {box_id}")
        if row["qty"] < qty:
            conn.close()
            raise Exception(f"Not enough stock in box {box_id} for {code}")
        # deduct
        new_qty = row["qty"] - qty
        cur.execute("UPDATE stock_ledger SET qty=? WHERE code=? AND box_id=?", (new_qty, code, box_id))
        # log pick
        cur.execute(
            "INSERT INTO stock_movements (code, box_id, qty, ref_type, ref_id) VALUES (?,?,?,?,?)",
            (code, box_id, qty, ref_type, ref_id)
        )
    conn.commit()
    conn.close()
    return {"code": code, "picks": picks, "status": "picked"}
