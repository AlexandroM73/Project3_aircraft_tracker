"""Тесты для утилит вывода."""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import io
from contextlib import redirect_stdout

import utils


class TestUtils(unittest.TestCase):
    def test_print_countries_count(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            utils.print_countries_count([("Germany", 15), ("Spain", 8)])
        self.assertIn("Germany", buf.getvalue())
        self.assertIn("15", buf.getvalue())

    def test_print_countries_count_empty(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            utils.print_countries_count([])
        self.assertIn("Нет данных", buf.getvalue())

    def test_print_aeroplanes(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            utils.print_aeroplanes([("abc123", "UAL123", "United States", -5.0, 55.0, 10000, 200, False)])
        self.assertIn("abc123", buf.getvalue())

    def test_print_avg_speed(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            utils.print_avg_speed(215.5)
        self.assertIn("215.50", buf.getvalue())

    def test_print_avg_speed_none(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            utils.print_avg_speed(None)
        self.assertIn("Нет данных", buf.getvalue())

    def test_print_higher_speed(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            utils.print_higher_speed([("abc123", "UAL123", "United States", 250.0)])
        self.assertIn("abc123", buf.getvalue())

    def test_print_keyword_search(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            utils.print_keyword_search([("def456", "ACA456", "Canada", 250.0)], "ACA")
        self.assertIn("def456", buf.getvalue())

    def test_print_keyword_search_empty(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            utils.print_keyword_search([], "ZZZ")
        self.assertIn("не найдены", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
