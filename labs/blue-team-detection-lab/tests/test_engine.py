import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import detect, normalize
from generate_demo import demo

class DetectionTests(unittest.TestCase):
    def test_all_three_rules(self):
        alerts = detect(demo())
        self.assertEqual({a["rule"] for a in alerts},
                         {"AUTH_BURST", "PORT_SCAN", "SUSPICIOUS_PROCESS"})

    def test_deterministic(self):
        self.assertEqual(detect(demo()), detect(list(reversed(demo()))))

    def test_reject_bad_ip(self):
        event = demo()[0] | {"source_ip": "not-an-ip"}
        with self.assertRaises(ValueError):
            normalize(event)

    def test_reject_invalid_port(self):
        event = next(x for x in demo() if x["type"] == "connection") | {"dest_port": 0}
        with self.assertRaises(ValueError):
            normalize(event)

    def test_auth_below_threshold(self):
        inputs = [x for x in demo() if x["type"] == "authentication"][:4]
        self.assertEqual(detect(inputs), [])

    def test_window(self):
        self.assertFalse(any(a["rule"] == "AUTH_BURST"
             for a in detect(demo(), window_minutes=0.01)))

if __name__ == "__main__":
    unittest.main()
