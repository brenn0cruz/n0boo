import unittest
from monitor import evaluate

class MonitorTests(unittest.TestCase):
    def transfer(self, finish="2026-01-01T00:02:00Z", status="success"):
        return {"transfer_id": "demo-1", "started_at": "2026-01-01T00:00:00Z",
                "finished_at": finish, "status": status}

    def test_pass(self):
        x = evaluate([self.transfer()])
        self.assertEqual((x["failed"], x["p95_seconds"]), (0, 120))

    def test_sla_breach(self):
        self.assertEqual(evaluate([self.transfer("2026-01-01T00:06:00Z")])["failed"], 1)

    def test_error(self):
        self.assertEqual(evaluate([self.transfer(status="error")])["failed"], 1)

    def test_negative_duration(self):
        with self.assertRaises(ValueError):
            evaluate([self.transfer("2025-12-31T23:59:00Z")])

if __name__ == "__main__":
    unittest.main()
