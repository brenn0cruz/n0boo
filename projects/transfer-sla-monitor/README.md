# Transfer SLA Monitor

A vendor-neutral, synthetic file-transfer SLA analytics exercise. Validates timezone-aware timestamps, calculates transfer latency, classifies SLA breaches and summarizes p95/p99 latencies via interpolation.

```bash
python monitor.py transfers.example.json
python -m unittest discover -s . -p 'test_*.py'
```

No bank names, infrastructure, hostnames, vendor identifiers, credentials, production logs or actual customer information. This is not connected to any employer system.
