"""Loopback-only lab API and browser dashboard."""
import os
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from engine import detect, normalize
from storage import all_events, counts, list_alerts, replace_alerts, save_events

app = FastAPI(title="Blue Team Detection Lab", version="1.0.0",
              docs_url="/docs", redoc_url=None)
TOKEN = os.environ.get("LAB_TOKEN", "")
MAX_BATCH = 500

class IngestRequest(BaseModel):
    events: list[dict] = Field(min_length=1, max_length=MAX_BATCH)

def authorize(token):
    # Optional lab token. Docker example sets it; never deploy publicly.
    if TOKEN and token != TOKEN:
        raise HTTPException(status_code=401, detail="invalid lab token")

@app.get("/health")
def health():
    return {"status": "ok", "mode": "synthetic-lab"}

@app.get("/api/stats")
def stats(x_lab_token: str | None = Header(default=None)):
    authorize(x_lab_token)
    return counts()

@app.get("/api/alerts")
def alerts(x_lab_token: str | None = Header(default=None)):
    authorize(x_lab_token)
    return list_alerts()

@app.post("/api/events")
def ingest(payload: IngestRequest, x_lab_token: str | None = Header(default=None)):
    authorize(x_lab_token)
    try:
        records = [normalize(e) for e in payload.events]
    except (ValueError, TypeError, OverflowError) as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    save_events(records)
    # Recompute from stored synthetic events; suitable for a bounded demo.
    new_alerts = detect(all_events())
    replace_alerts(new_alerts)
    return {"accepted": len(records), "alerts": len(new_alerts)}

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return (Path(__file__).parent / "dashboard.html").read_text(encoding="utf-8")
