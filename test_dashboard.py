import unittest
import base64
from unittest.mock import patch
from urllib.error import HTTPError

from dashboard import main, render


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

    def test_conflict_rereads_readme_before_retry(self):
        readme = "<!-- DASHBOARD_START -->\n<!-- DASHBOARD_END -->"
        reads = iter([(readme, "old"), ("Owner edit\n" + readme, "new")])
        writes = []

        def fake_api(path, data=None):
            if data is None:
                content, sha = next(reads)
                return {"content": base64.b64encode(content.encode()).decode(), "sha": sha}
            writes.append(data)
            if len(writes) == 1:
                raise HTTPError(path, 409, "Conflict", {}, None)
            return {}

        with patch("dashboard.api", side_effect=fake_api), patch("dashboard.prospect_issues", return_value=[]):
            main()
        self.assertEqual([write["sha"] for write in writes], ["old", "new"])
        self.assertTrue(base64.b64decode(writes[1]["content"]).decode().startswith("Owner edit\n"))


if __name__ == "__main__":
    unittest.main()

