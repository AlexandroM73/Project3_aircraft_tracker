"""Тесты для APIAdapter (requests мокируется)."""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from unittest.mock import patch, MagicMock

from api_adapter import APIAdapter


class TestAPIAdapter(unittest.TestCase):
    """Тесты получения границ стран и самолетов через API."""

    @patch("api_adapter.requests.Session")
    def setUp(self, mock_session_cls):
        self.mock_session = MagicMock()
        mock_session_cls.return_value = self.mock_session
        self.adapter = APIAdapter()

    def test_get_country_bbox_success(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = [{"boundingbox": ["51.0", "60.0", "-10.0", "2.0"]}]
        mock_resp.raise_for_status = MagicMock()
        self.mock_session.get.return_value = mock_resp
        result = self.adapter.get_country_bbox("France")
        self.assertEqual(result, [51.0, 60.0, -10.0, 2.0])

    def test_get_country_bbox_not_found(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        self.mock_session.get.return_value = mock_resp
        result = self.adapter.get_country_bbox("NonExistent")
        self.assertIsNone(result)

    def test_get_country_bbox_network_error(self):
        import requests as req
        self.mock_session.get.side_effect = req.RequestException("err")
        result = self.adapter.get_country_bbox("France")
        self.assertIsNone(result)

    def test_get_aeroplanes_success(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"states": [
            ["abc123", "UAL123", "United States", None, None, -5.0, 55.0, 10000, 200, 90, 0, False, "1234", False],
            ["ghi789", None, "United States", None, None, None, None, None, None, None, None, True, None, False],
        ]}
        mock_resp.raise_for_status = MagicMock()
        self.mock_session.get.return_value = mock_resp
        result = self.adapter.get_aeroplanes_in_bbox(50, 60, -10, 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "abc123")

    def test_get_aeroplanes_empty(self):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"states": []}
        mock_resp.raise_for_status = MagicMock()
        self.mock_session.get.return_value = mock_resp
        result = self.adapter.get_aeroplanes_in_bbox(0, 90, 0, 180)
        self.assertEqual(result, [])

    def test_get_aeroplanes_network_error(self):
        import requests as req
        self.mock_session.get.side_effect = req.RequestException("timeout")
        result = self.adapter.get_aeroplanes_in_bbox(0, 90, 0, 180)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
