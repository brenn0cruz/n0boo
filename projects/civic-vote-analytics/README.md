# Civic Vote Analytics

Nonpartisan roll-call voting aggregation exercise using **fictional example parties and members**. Summarizes yes/no/abstain/absent votes and party breakdowns, and explicitly excludes abstentions and absences from the decisive-vote denominator.

```bash
python analyzer.py votes.example.json
python -m unittest discover -s . -p 'test_*.py'
```

## Next steps
Add documented adapters for official legislative open-data APIs, freshness timestamps, ingestion tests and data-source attribution before claiming real-world coverage. No live voting or political classification is implemented.
