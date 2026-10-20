import unittest
from correlator import correlate

class CorrelatorTests(unittest.TestCase):
    def event(self, minute, ip="192.0.2.4", result="failure"):
        return {"timestamp": f"2026-01-01T00:{minute:02d}:00Z",
                "source_ip": ip, "event_type": "authentication", "result": result}

    def test_burst(self):
        self.assertEqual(len(correlate([self.event(i) for i in range(5)])), 1)

    def test_below_threshold(self):
        self.assertEqual(correlate([self.event(i) for i in range(4)]), [])

    def test_separated_ip(self):
        ev = [self.event(i, "192.0.2.1") for i in range(3)]
        ev += [self.event(i, "192.0.2.2") for i in range(3)]
        self.assertEqual(correlate(ev), [])

    def test_time_window(self):
        ev = [self.event(i) for i in [0, 1, 2, 12, 13]]
        self.assertEqual(correlate(ev), [])

    def test_missing_fields(self):
        with self.assertRaises(ValueError):
            correlate([{"timestamp": "2026-01-01T00:00:00Z"}])

if __name__ == "__main__":
    unittest.main()
