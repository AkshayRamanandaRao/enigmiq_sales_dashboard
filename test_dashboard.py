import unittest

from dashboard import render


class DashboardTest(unittest.TestCase):
    def test_counts_and_daily_history_are_idempotent(self):
        readme = "Before\n<!-- DASHBOARD_START -->\n<!-- DASHBOARD_END -->\nAfter"
        issues = [{"title": "[meeting] Acme Engineering", "body": "Next action: 2026-11-10 demo", "html_url": "https://github.com/example/repo/issues/1"}]
        first = render(readme, issues, "2026-11-08")
        second = render(first, issues, "2026-11-08")
        self.assertEqual(first, second)
        self.assertIn("| 2026-11-08 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |", first)
        self.assertIn("2026-11-10 demo", first)
        self.assertTrue(first.startswith("Before\n"))
        self.assertTrue(first.endswith("\nAfter"))


if __name__ == "__main__":
    unittest.main()

