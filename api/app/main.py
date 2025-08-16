from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
from api.app import db, crud_import

app = FastAPI(title="SurgicalOps API")

# Allow CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS FOR SIMPLE TEST ---
class StockPick(BaseModel):
    code: str
    picks: List[Dict]  # [{"box_id": "B-001", "qty": 10}]
    ref_type: str = "pick"
    ref_id: str

# --- ROUTES ---

@app.get("/")
def root():
    return {"status": "ok", "message": "SurgicalOps API running."}

@app.post("/stock/pick")
def stock_pick(pick: StockPick):
    try:
        result = db.pick_stock(pick.code, pick.picks, pick.ref_type, pick.ref_id)
        return {"status": "success", "details": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stock/available")
def stock_available(code: str):
    try:
        stock = db.get_available_stock(code)
        return {"status": "success", "stock": stock}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/import/excel")
def import_excel():
    try:
        result = crud_import.import_all("./data/surgicalops.db", "./data")
        return {"status": "success", "details": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Future endpoints for PO, Vendor Images, Pricing etc. will be added here

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
