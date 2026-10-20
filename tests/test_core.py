import unittest
from ssi.core import Source, investigate

class Search:
    def search(self, query, limit):
        self.query, self.limit = query, limit
        return [Source("Test", "https://example.org/report", "An illustrative excerpt"),
                Source("Duplicate", "https://example.org/report", "Same page")]

class Analyzer:
    def analyze(self, query, sources):
        return "Insufficient evidence for a conclusion.", [], ["Example fixture only"]

class PipelineTests(unittest.TestCase):
    def test_query_to_report(self):
        search = Search()
        report = investigate("  AI security incidents  ", "normal", search, Analyzer())
        self.assertEqual(report.query, "AI security incidents")
        self.assertEqual(search.limit, 5)
        self.assertEqual(len(report.sources), 1)
        self.assertIn("Insufficient evidence", report.summary)
        self.assertIn('"query": "AI security incidents"', report.to_json())

    def test_invalid_query(self):
        with self.assertRaises(ValueError):
            investigate("", "normal", Search(), Analyzer())

    def test_invalid_depth(self):
        with self.assertRaises(ValueError):
            investigate("test", "unlimited", Search(), Analyzer())

if __name__ == "__main__":
    unittest.main()
