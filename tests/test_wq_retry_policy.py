import unittest

import requests

from app.services.wq_retry_policy import (
    RemoteWaitDecision,
    classify_post_exception,
    next_wait_seconds,
    should_retry_without_skipping,
)


class WQRetryPolicyTests(unittest.TestCase):
    def test_429_uses_short_wait_except_each_fifth_failure(self):
        self.assertEqual(next_wait_seconds(1, short_seconds=30, long_seconds=600), 30)
        self.assertEqual(next_wait_seconds(4, short_seconds=30, long_seconds=600), 30)
        self.assertEqual(next_wait_seconds(5, short_seconds=30, long_seconds=600), 600)
        self.assertEqual(next_wait_seconds(6, short_seconds=30, long_seconds=600), 30)

    def test_network_disconnect_is_retryable_without_skip(self):
        exc = requests.exceptions.ConnectionError("Remote end closed connection without response")

        decision = classify_post_exception(exc, failure_count=3, long_wait_seconds=600)

        self.assertEqual(decision, RemoteWaitDecision("network", 600, "network_disconnect"))
        self.assertTrue(should_retry_without_skipping(decision))

    def test_payload_error_is_not_retryable_without_skip(self):
        decision = classify_post_exception(RuntimeError("status=400 body=bad expression"), failure_count=1)

        self.assertEqual(decision.reason, "non_retryable")
        self.assertFalse(should_retry_without_skipping(decision))


if __name__ == "__main__":
    unittest.main()
