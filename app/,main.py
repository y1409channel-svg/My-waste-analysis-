from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.database import SessionLocal, WasteRecord
from app.ai_analysis import analyze_waste
import pandas as pd

app = FastAPI(title="Cheese Waste Management System")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/api/waste")
def add_waste(total_waste: float, usable_waste: float):
    db = SessionLocal()
    record = WasteRecord(
        total_waste=total_waste,
        usable_waste=usable_waste,
        unusable_waste=total_waste - usable_waste
    )
    db.add(record)
    db.commit()
    db.close()
    return {"status": "Waste recorded"}

@app.get("/api/analysis")
def analysis():
    db = SessionLocal()
    records = db.query(WasteRecord).all()
    db.close()

    if not records:
        return {"message": "No data yet"}

    df = pd.DataFrame([{
        "total": r.total_waste,
        "usable": r.usable_waste,
        "unusable": r.unusable_waste
    } for r in records])

    return analyze_waste(df)
