import unittest
from analyzer import analyze

class AnalyzerTests(unittest.TestCase):
    def test_count(self):
        result = analyze([{"member_id":1,"party":"A","vote":"yes"},
                          {"member_id":2,"party":"A","vote":"no"},
                          {"member_id":3,"party":"B","vote":"absent"}])
        self.assertEqual(result["yes_share_of_decisive_votes"], .5)
        self.assertEqual(result["by_party"]["A"]["no"], 1)

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            analyze([{"member_id":1,"party":"A","vote":"yes"}]*2)

    def test_no_decisive_votes(self):
        self.assertIsNone(analyze([])["yes_share_of_decisive_votes"])

if __name__ == "__main__":
    unittest.main()
