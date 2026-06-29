import unittest
from unittest.mock import MagicMock
import requests
from app.services.wq_client import retire_wq_alpha


class WQClientTests(unittest.TestCase):
    def test_retire_wq_alpha_success(self):
        session = MagicMock()
        response = MagicMock()
        response.status_code = 204
        session.delete.return_value = response

        result = retire_wq_alpha(session, "test_alpha_id")
        self.assertTrue(result)
        session.delete.assert_called_once_with(
            "https://api.worldquantbrain.com/simulations/test_alpha_id",
            timeout=30
        )

    def test_retire_wq_alpha_already_deleted(self):
        session = MagicMock()
        response = MagicMock()
        response.status_code = 404
        session.delete.return_value = response

        result = retire_wq_alpha(session, "test_alpha_id")
        self.assertTrue(result)

    def test_retire_wq_alpha_failure(self):
        session = MagicMock()
        response = MagicMock()
        response.status_code = 500
        session.delete.return_value = response

        result = retire_wq_alpha(session, "test_alpha_id")
        self.assertFalse(result)

    def test_retire_wq_alpha_exception(self):
        session = MagicMock()
        session.delete.side_effect = Exception("Network error")

        result = retire_wq_alpha(session, "test_alpha_id")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
