import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path to import requester
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import requester


class TestRequester(unittest.TestCase):
    @patch("requester.requests.get")
    def test_make_request_success(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call function with no failure rate
        result = requester.make_request("https://example.com/api", 0, [])

        # Check the request was made
        mock_get.assert_called_once_with("https://example.com/api", timeout=5)

        # Check the result is success
        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)

    def test_should_simulate_failure(self):
        # With 100% failure rate, should always return True
        self.assertTrue(requester.should_simulate_failure(100))

        # With 0% failure rate, should always return False
        self.assertFalse(requester.should_simulate_failure(0))

    @patch("requester.random.choice")
    @patch("requester.should_simulate_failure")
    @patch("requester.requests.get")
    def test_make_request_simulated_500(
        self, mock_get, mock_should_simulate_failure, mock_choice
    ):
        # Setup mocks to simulate a 500 error
        mock_should_simulate_failure.return_value = True
        mock_choice.return_value = "500"

        # Call function with 100% failure rate
        result = requester.make_request("https://example.com/api", 100, ["500"])

        # Check the request was not made (we're simulating the error)
        mock_get.assert_not_called()

        # Check the result is failure with proper error
        self.assertFalse(result["success"])
        self.assertEqual(result["status_code"], 500)
        self.assertEqual(result["error"], "Simulated 500 error")


if __name__ == "__main__":
    unittest.main()
