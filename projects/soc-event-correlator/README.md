# SOC Event Correlator

Educational blue-team detection prototype. Ingests JSONL authentication events, normalizes UTC timestamps, groups failures per source IP, detects bursts within a sliding time window and outputs structured alerts.

## Run
```bash
python correlator.py events.example.jsonl --threshold 5
python -m unittest discover -s . -p 'test_*.py'
```

**Design:** standard library, deterministic processing, idempotent handling for events with IDs, input validation, no network calls. IPs and events are synthetic. This is a learning implementation, not a production SIEM.
