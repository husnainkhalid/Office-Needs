# api/app/routes_inventory.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

router = APIRouter(prefix="/inventory", tags=["inventory"])

DB_PATH = "./data/surgicalops.db"

def db():
    return sqlite3.connect(DB_PATH)

class PickLine(BaseModel):
    box_id: str
    qty: int

class PickRequest(BaseModel):
    code: str
    picks: List[PickLine]  # [{box_id, qty}]
    ref_type: str = "pick"
    ref_id: str = "UI"

class AddRequest(BaseModel):
    code: str
    box_id: str
    qty: int
    note: Optional[str] = None

class MoveRequest(BaseModel):
    code: str
    from_box: str
    to_box: str
    qty: int

@router.get("/available")
def available(code: str):
    con = db()
    cur = con.cursor()
    cur.execute("""
        SELECT box_id, COALESCE(SUM(qty_in - qty_out),0) AS qty
        FROM stock_ledger
        WHERE code = ?
        GROUP BY box_id
        HAVING qty > 0
        ORDER BY box_id
    """, (code,))
    rows = [{"box_id": r[0], "qty": r[1]} for r in cur.fetchall()]
    con.close()
    return {"status": "success", "stock": rows}

@router.post("/add")
def add_stock(req: AddRequest):
    if req.qty <= 0:
        raise HTTPException(400, "qty must be > 0")
    con = db()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO stock_ledger (code, box_id, qty_in, qty_out, ref_type, ref_id, note)
        VALUES (?, ?, ?, 0, 'manual_add', 'UI', ?)
    """, (req.code, req.box_id, req.qty, req.note or ""))
    con.commit()
    con.close()
    return {"status": "success"}

@router.post("/pick")
def pick(req: PickRequest):
    con = db()
    cur = con.cursor()
    # validate stock
    for line in req.picks:
        cur.execute("""
            SELECT COALESCE(SUM(qty_in - qty_out),0) FROM stock_ledger
            WHERE code=? AND box_id=?
        """, (req.code, line.box_id))
        avail = cur.fetchone()[0]
        if line.qty > avail:
            con.close()
            raise HTTPException(400, f"Not enough stock in {line.box_id}: have {avail}, need {line.qty}")
    # write picks
    for line in req.picks:
        cur.execute("""
            INSERT INTO stock_ledger (code, box_id, qty_in, qty_out, ref_type, ref_id)
            VALUES (?, ?, 0, ?, ?, ?)
        """, (req.code, line.box_id, line.qty, req.ref_type, req.ref_id))
    con.commit()
    con.close()
    return {"status": "success"}

@router.post("/move")
def move(req: MoveRequest):
    if req.qty <= 0:
        raise HTTPException(400, "qty must be > 0")
    # perform pick from from_box and add to to_box
    pick(req=PickRequest(code=req.code, picks=[PickLine(box_id=req.from_box, qty=req.qty)], ref_type="move", ref_id=f"{req.from_box}->{req.to_box}"))
    add_stock(req=AddRequest(code=req.code, box_id=req.to_box, qty=req.qty, note=f"move from {req.from_box}"))
    return {"status": "success"}
