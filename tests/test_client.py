import unittest
from unittest.mock import patch, MagicMock
from client.status_client import StatusClient

class TestStatusClient(unittest.TestCase):

    @patch('client.status_client.requests.get')
    def test_status_completed(self, mock_get):
        # Simulate a "completed" response from the server
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "completed"}
        mock_get.return_value = mock_response

        client = StatusClient("http://fake-url.com")
        result = client.check_status()

        self.assertEqual(result, "completed")
    
    @patch('client.status_client.requests.get')
    def test_status_pending_then_completed(self, mock_get):
        # Simulate a "pending" response followed by a "completed" response
        mock_response_pending = MagicMock()
        mock_response_pending.json.return_value = {"result": "pending"}
        mock_response_completed = MagicMock()
        mock_response_completed.json.return_value = {"result": "completed"}

        # Mock the sequence of responses
        mock_get.side_effect = [mock_response_pending, mock_response_completed]

        client = StatusClient("http://fake-url.com", retries=2, initial_backoff=1)
        result = client.check_status()

        self.assertEqual(result, "completed")

    @patch('client.status_client.requests.get')
    def test_status_error(self, mock_get):
        # Simulate an "error" response from the server
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "error"}
        mock_get.return_value = mock_response

        client = StatusClient("http://fake-url.com")
        result = client.check_status()

        self.assertEqual(result, "error")

    @patch('client.status_client.requests.get')
    def test_max_retries_reached(self, mock_get):
        # Simulate a "pending" response continuously
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "pending"}
        mock_get.return_value = mock_response

        client = StatusClient("http://fake-url.com", retries=3, initial_backoff=1)
        result = client.check_status()

        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
