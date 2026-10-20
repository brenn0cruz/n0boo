# Blue Team Detection Lab 🛡️

**A reproducible, local-only cybersecurity detection range:** synthetic event generator → validation → SQLite store → detection engine → REST API → dashboard.

> Status: educational v1.0. No real network scanning, exploit delivery, endpoint agents, corporate datasets or production integrations.

## Architecture

```text
[synthetic event generator] -> [validation & normalization]
                                       |
                                       v
                                [SQLite events]
                                       |
                                       v
                    [detector: 5-minute rolling windows]
                           |               |
                       [alerts] --> [SQLite alerts]
                                          |
                                     [FastAPI]
                                       /   \
                              [JSON endpoints] [HTML dashboard]
```

**Detections**: five failed logins from one source to one host; eight different destination ports by the same source; high-risk process names in simulated telemetry. Uses TEST-NET IP ranges reserved for documentation.

## Quick start

Requires Docker Compose. From this directory:

```bash
cp .env.example .env
# Edit .env and set LAB_TOKEN to a strong random value; never commit it
docker compose up --build -d
```

Browse **http://127.0.0.1:8080**. Enter the value of LAB_TOKEN in the dashboard and click **Refresh dashboard**. Initial synthetic data are seeded automatically. OpenAPI docs: **http://127.0.0.1:8080/docs**.

API examples (replace token):
```bash
curl -H 'X-Lab-Token: YOUR_LOCAL_TOKEN' http://127.0.0.1:8080/api/stats
curl -H 'X-Lab-Token: YOUR_LOCAL_TOKEN' http://127.0.0.1:8080/api/alerts
```

Generate additional offline demo data: `python generate_demo.py`. Post JSON matching `{"events": [...]}` to `POST /api/events` using the same token header.

Run detection tests without third-party packages: `python -m unittest discover -s tests -v`.

## API

| Route | Purpose |
| --- | --- |
| `GET /health` | health check |
| `GET /api/stats` | event and alert counters |
| `GET /api/alerts` | latest 100 alerts |
| `POST /api/events` | ingest up to 500 JSON events, deduplicated by ID |

## Security boundaries

- Binds to **127.0.0.1 only** on the Docker host; never expose the port publicly.
- Optional token authentication becomes mandatory in the supplied Compose deployment.
- Runs as a non-root container, drops Linux capabilities and uses a read-only filesystem.
- Stores only synthetic telemetry, not company secrets, customer data or access logs.
- SQLite model and full recomputation are deliberately sized for learning; not intended for high-volume production ingestion.
- The rule matching a process name is a simulation signal, not proof of compromise.
- Do not commit your `.env` file.

## Limitations and roadmap

Rules are intentionally simplified; no streaming broker, RBAC, TLS reverse proxy, correlation across persistent time buckets, retention policy, telemetry signing or production alert workflow. Next: MITRE ATT&CK mapping, pluggable Sigma-like rules, replay mode, coverage metrics, CI container tests and realistic analyst case management.

## Portfolio narrative

Demonstrates secure defaults, container deployment, defensive detection engineering, typed API boundary, state persistence, rule testing, REST design and human-readable operational visualization. All examples are original lab scenarios, not recreations of employer systems.

License: MIT (see LICENSE).
