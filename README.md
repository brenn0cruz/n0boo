# Brenno Cruz | Cybersecurity, Engineering & Technology

Building reliable, measurable systems at the intersection of **security engineering, infrastructure, automation and business technology**.

Experience across application support and technology operations; interested in solutions engineering, cybersecurity and technical consulting.


## Cybersecurity lab

**[Blue Team Detection Lab](labs/blue-team-detection-lab)** — a local-only, containerized security operations range with synthetic telemetry, a Python detection engine, SQLite, FastAPI, and an interactive dashboard. Includes authentication-burst, simulated port-sweep and suspicious-process alert rules. [Architecture and quick start →](labs/blue-team-detection-lab/README.md)

## Featured technical portfolio

| Project | Engineering focus | Stack |
| --- | --- | --- |
| [SOC Event Correlator](projects/soc-event-correlator) | Event normalization, sliding-window detection, structured alerts, unit tests | Python |
| [Transfer SLA Monitor](projects/transfer-sla-monitor) | Operational observability, latency percentiles, SLA evaluation | Python |
| [Civic Vote Analytics](projects/civic-vote-analytics) | Nonpartisan roll-call aggregation, validation and reporting | Python |

Each repository module includes runnable examples, tests and a dedicated README. These are **educational, independently authored demonstrations**, not replicas of any employer or client system.

### Technical interests
- Cybersecurity: detection engineering, defensive security, risk and security operations
- Systems: Windows, Linux, networking, troubleshooting and automation
- Engineering: Python, SQL, APIs, reliability and observability
- Business technology: solutions consulting, technical discovery and translating requirements into solutions

### Run the test suites
```bash
cd projects/soc-event-correlator && python -m unittest discover -s . -p 'test_*.py'
cd ../transfer-sla-monitor && python -m unittest discover -s . -p 'test_*.py'
cd ../civic-vote-analytics && python -m unittest discover -s . -p 'test_*.py'
```

### Privacy & responsible disclosure
Only fictional, synthetic or expressly public demonstration data are used in the portfolio. Do not commit credentials, operational records, client data, internal configurations or proprietary source code.

[LinkedIn](https://www.linkedin.com/in/brennocruz/)
