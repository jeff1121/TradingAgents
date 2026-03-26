"""CLI config 的單元測試。"""

import unittest

from cli.config import CLI_CONFIG


class TestCLIConfig(unittest.TestCase):
    def test_is_dict(self):
        self.assertIsInstance(CLI_CONFIG, dict)

    def test_announcements_url(self):
        self.assertIn("announcements_url", CLI_CONFIG)
        self.assertTrue(CLI_CONFIG["announcements_url"].startswith("http"))

    def test_announcements_timeout(self):
        self.assertIn("announcements_timeout", CLI_CONFIG)
        self.assertIsInstance(CLI_CONFIG["announcements_timeout"], float)

    def test_announcements_fallback(self):
        self.assertIn("announcements_fallback", CLI_CONFIG)
        self.assertIsInstance(CLI_CONFIG["announcements_fallback"], str)


if __name__ == "__main__":
    unittest.main()
