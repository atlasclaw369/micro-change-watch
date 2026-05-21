import unittest

from scripts.change_watch import plan_limit, validate_customer_config, validate_public_url


class ValidationTests(unittest.TestCase):
    def test_plan_limits_are_enforced(self):
        cfg = {
            "customer": "TooMany",
            "plan": "starter",
            "cadence": "daily",
            "urls": ["https://example.com/a", "https://example.com/b", "https://example.com/c", "https://example.com/d"],
        }
        self.assertTrue(any("allows at most 3 URLs" in problem for problem in validate_customer_config(cfg)))

    def test_known_plan_names_map_to_limits(self):
        self.assertEqual(plan_limit("$9/month — Starter: 3 URLs"), 3)
        self.assertEqual(plan_limit("$19/month — Standard: 10 URLs"), 10)
        self.assertEqual(plan_limit("$10 one-off — 48-hour watch: 5 URLs"), 5)

    def test_secret_like_query_keys_are_rejected(self):
        problems = validate_public_url("https://example.com/changelog?signature=abc123")
        self.assertTrue(any("secret/token" in problem for problem in problems))

    def test_private_and_embedded_credentials_are_rejected(self):
        self.assertTrue(validate_public_url("http://localhost:8000/status"))
        problems = validate_public_url("https://user:pass@example.com/docs")
        self.assertTrue(any("embedded credentials" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
