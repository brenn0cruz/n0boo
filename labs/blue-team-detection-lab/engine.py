"""Deterministic detection rules for synthetic security telemetry."""
from collections import defaultdict, deque
from datetime import datetime, timezone, timedelta
from ipaddress import ip_address

TYPES = {"authentication", "connection", "process"}
SEVERITIES = {"AUTH_BURST": "high", "PORT_SCAN": "medium", "SUSPICIOUS_PROCESS": "high"}

def normalize(record):
    required = ("event_id", "timestamp", "host", "source_ip", "type")
    if any(not isinstance(record.get(k), str) or not record[k].strip() for k in required):
        raise ValueError("missing required string event field")
    if record["type"] not in TYPES:
        raise ValueError("unsupported event type")
    stamp = datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    ip_address(record["source_ip"])
    if len(record["event_id"]) > 128 or len(record["host"]) > 128:
        raise ValueError("field too long")
    if record["type"] == "connection":
        port = record.get("dest_port")
        if type(port) is not int or not 1 <= port <= 65535:
            raise ValueError("invalid destination port")
    if record["type"] == "authentication" and record.get("outcome") not in ("success", "failure"):
        raise ValueError("invalid auth outcome")
    if record["type"] == "process" and not isinstance(record.get("process_name"), str):
        raise ValueError("missing process name")
    result = {k: record.get(k) for k in (
        "event_id", "host", "source_ip", "type", "outcome", "dest_port", "process_name"
    )}
    result["timestamp"] = stamp.astimezone(timezone.utc).isoformat()
    return result

def detection_key(rule, source_ip, host, end_time):
    return "|".join((rule, source_ip, host, end_time))

def detect(records, auth_threshold=5, scan_threshold=8, window_minutes=5):
    """Return deterministic alert records; never executes network operations."""
    if min(auth_threshold, scan_threshold, window_minutes) <= 0:
        raise ValueError("thresholds must be positive")
    events = sorted((normalize(r) for r in records), key=lambda r: (r["timestamp"], r["event_id"]))
    auth = defaultdict(deque)
    ports = defaultdict(deque)
    emitted = set()
    alerts = []
    for e in events:
        ts = datetime.fromisoformat(e["timestamp"])
        cutoff = ts - timedelta(minutes=window_minutes)
        group = (e["source_ip"], e["host"])
        candidates = []
        if e["type"] == "authentication" and e["outcome"] == "failure":
            q = auth[group]
            while q and q[0] < cutoff:
                q.popleft()
            q.append(ts)
            if len(q) >= auth_threshold:
                candidates.append(("AUTH_BURST", f"{len(q)} failed logins in {window_minutes}m"))
        elif e["type"] == "connection":
            q = ports[group]
            while q and q[0][0] < cutoff:
                q.popleft()
            q.append((ts, e["dest_port"]))
            if len({port for _, port in q}) >= scan_threshold:
                candidates.append(("PORT_SCAN", f"{len({port for _, port in q})} distinct destination ports"))
        elif e["type"] == "process" and e["process_name"].lower() in ("mimikatz.exe", "procdump.exe"):
            candidates.append(("SUSPICIOUS_PROCESS", "Known high-risk tool name in synthetic telemetry"))
        for rule, detail in candidates:
            # Emit once per rule/source/host in the dataset, instead of flooding.
            dedup = (rule, *group)
            if dedup in emitted:
                continue
            emitted.add(dedup)
            alerts.append({"alert_id": detection_key(rule, *group, e["timestamp"]),
                           "rule": rule, "severity": SEVERITIES[rule], "source_ip": group[0],
                           "host": group[1], "timestamp": e["timestamp"],
                           "evidence": detail})
    return alerts
