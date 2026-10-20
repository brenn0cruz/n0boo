"""Creates only synthetic events. No scanning, probing or host discovery."""
import json
from datetime import datetime, timedelta, timezone
from engine import normalize

def demo():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    events = []
    def add(kind, idx, seconds, ip, **fields):
        events.append(normalize({"event_id": f"{kind}-{idx}",
            "timestamp": (start + timedelta(seconds=seconds)).isoformat(),
            "host": "demo-workstation", "source_ip": ip, "type": kind, **fields}))
    for i in range(7):
        add("authentication", i, i*20, "192.0.2.10", outcome="failure")
    for i in range(10):
        add("connection", i, 200+i*10, "198.51.100.9", dest_port=10000+i)
    add("process", 0, 400, "203.0.113.4", process_name="procdump.exe")
    add("authentication", 8, 450, "192.0.2.11", outcome="success")
    return events

if __name__ == "__main__":
    from pathlib import Path
    path=Path("data")/"events.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(demo(), indent=2), encoding="utf-8")
    print(f"Wrote {len(demo())} synthetic events to {path}")
