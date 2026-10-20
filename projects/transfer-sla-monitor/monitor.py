"""Transfer SLA evaluator with synthetic operational data."""
from datetime import datetime, timezone
from statistics import quantiles

def normalize_timestamp(value):
    stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise ValueError("timezone required")
    return stamp.astimezone(timezone.utc)

def evaluate(transfers, max_latency_seconds=300):
    if max_latency_seconds <= 0:
        raise ValueError("SLA must be positive")
    output = []
    latencies = []
    for item in transfers:
        started = normalize_timestamp(item["started_at"])
        finished = normalize_timestamp(item["finished_at"])
        latency = (finished - started).total_seconds()
        if latency < 0:
            raise ValueError("finished_at precedes started_at")
        status = "PASS" if item["status"] == "success" and latency <= max_latency_seconds else "FAIL"
        output.append({"transfer_id": item["transfer_id"], "latency_seconds": latency,
                       "status": status, "reason": "ok" if status == "PASS" else "transfer failure or SLA breach"})
        if item["status"] == "success":
            latencies.append(latency)
    ordered = sorted(latencies)
    def percentile(p):
        if not ordered:
            return None
        ix = (len(ordered) - 1) * p
        low = int(ix)
        return round(ordered[low] + (ordered[min(low + 1, len(ordered)-1)] - ordered[low]) * (ix-low), 2)
    return {"total": len(output), "failed": sum(x["status"] == "FAIL" for x in output),
            "p95_seconds": percentile(.95), "p99_seconds": percentile(.99),
            "transfers": output}

if __name__ == "__main__":
    import json, sys
    with open(sys.argv[1], encoding="utf-8") as stream:
        data = json.load(stream)
    print(json.dumps(evaluate(data), indent=2))
