"""SQLite persistence; no external data collection."""
import json
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.environ.get("LAB_DB", "/tmp/blue_team_lab.db"))

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=3000")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS events (
        event_id TEXT PRIMARY KEY, timestamp TEXT NOT NULL, type TEXT NOT NULL,
        host TEXT NOT NULL, source_ip TEXT NOT NULL, body TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS alerts (
        alert_id TEXT PRIMARY KEY, timestamp TEXT NOT NULL, rule TEXT NOT NULL,
        severity TEXT NOT NULL, source_ip TEXT NOT NULL, host TEXT NOT NULL, body TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_events_time ON events(timestamp);
    CREATE INDEX IF NOT EXISTS idx_alerts_time ON alerts(timestamp);
    """)
    return conn

def save_events(events):
    with connect() as conn:
        for item in events:
            conn.execute("INSERT OR IGNORE INTO events VALUES(?, ?, ?, ?, ?, ?)",
                         (item["event_id"], item["timestamp"], item["type"],
                          item["host"], item["source_ip"], json.dumps(item)))
    return len(events)

def all_events(limit=10000):
    with connect() as conn:
        result = conn.execute("SELECT body FROM events ORDER BY timestamp DESC, event_id DESC LIMIT ?",
                              (limit,)).fetchall()
    return [json.loads(row[0]) for row in result]

def replace_alerts(alerts):
    with connect() as conn:
        conn.execute("DELETE FROM alerts")
        for a in alerts:
            conn.execute("INSERT INTO alerts VALUES(?, ?, ?, ?, ?, ?, ?)",
                         (a["alert_id"], a["timestamp"], a["rule"], a["severity"],
                          a["source_ip"], a["host"], json.dumps(a)))

def list_alerts(limit=100):
    with connect() as conn:
        rows = conn.execute("SELECT body FROM alerts ORDER BY timestamp DESC LIMIT ?",
                            (limit,)).fetchall()
    return [json.loads(row[0]) for row in rows]

def counts():
    with connect() as conn:
        events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        alerts = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    return {"events": events, "alerts": alerts}
