"""Initialize the lab database from synthetic generator."""
from engine import detect
from generate_demo import demo
from storage import all_events, replace_alerts, save_events, counts

if __name__ == "__main__":
    records=demo()
    save_events(records)
    replace_alerts(detect(all_events()))
    print(counts())
