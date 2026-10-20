"""Small deterministic SOC event correlation engine; standard library only."""
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import json

def parse_event(raw):
    required = ("timestamp", "source_ip", "event_type", "result")
    if any(not raw.get(k) for k in required):
        raise ValueError("missing required event field")
    t = datetime.fromisoformat(raw["timestamp"].replace("Z", "+00:00"))
    if t.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return {**raw, "time": t.astimezone(timezone.utc)}

def correlate(records, threshold=5, window_minutes=10):
    """Flag repeated failed logins, suppressing duplicates and counting by IP."""
    if threshold < 1 or window_minutes <= 0:
        raise ValueError("invalid configuration")
    events = sorted((parse_event(x) for x in records), key=lambda x: x["time"])
    buckets = defaultdict(list)
    seen = set()
    alerts = []
    for ev in events:
        if ev["event_type"] != "authentication" or ev["result"] != "failure":
            continue
        key = (ev["time"], ev["source_ip"], ev.get("event_id"))
        if ev.get("event_id") and key in seen:
            continue
        seen.add(key)
        ip = ev["source_ip"]
        cutoff = ev["time"] - timedelta(minutes=window_minutes)
        buckets[ip] = [t for t in buckets[ip] if t >= cutoff]
        buckets[ip].append(ev["time"])
        if len(buckets[ip]) == threshold:
            alerts.append({"rule": "AUTH_FAILURE_BURST", "source_ip": ip,
                           "count": len(buckets[ip]), "start": buckets[ip][0].isoformat(),
                           "end": ev["time"].isoformat(), "severity": "medium"})
    return alerts

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("events", help="JSONL file of synthetic authentication events")
    p.add_argument("--threshold", type=int, default=5)
    args = p.parse_args()
    with open(args.events, encoding="utf-8") as stream:
        records = [json.loads(line) for line in stream if line.strip()]
    print(json.dumps(correlate(records, threshold=args.threshold), indent=2))
