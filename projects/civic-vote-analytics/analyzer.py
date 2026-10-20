"""Nonpartisan legislative roll-call aggregation from local public-format JSON."""
from collections import Counter

VALID = {"yes", "no", "abstain", "absent"}

def analyze(votes):
    seen = set()
    counts = Counter()
    party_counts = {}
    for item in votes:
        member = str(item["member_id"])
        if member in seen:
            raise ValueError("duplicate member")
        seen.add(member)
        vote = str(item["vote"]).lower()
        if vote not in VALID:
            raise ValueError("unsupported vote")
        party = str(item["party"])
        counts[vote] += 1
        if party not in party_counts:
            party_counts[party] = Counter()
        party_counts[party][vote] += 1
    participating = counts["yes"] + counts["no"]
    return {
        "totals": {v: counts[v] for v in sorted(VALID)},
        "yes_share_of_decisive_votes": round(counts["yes"]/participating, 4) if participating else None,
        "by_party": {p: {v: c[v] for v in sorted(VALID)} for p, c in sorted(party_counts.items())}
    }

if __name__ == "__main__":
    import json, sys
    with open(sys.argv[1], encoding="utf-8") as file:
        records = json.load(file)
    print(json.dumps(analyze(records), indent=2, ensure_ascii=False))
