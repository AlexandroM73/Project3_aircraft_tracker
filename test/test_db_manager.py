"""Тесты для DBManager (psycopg2 мокируется)."""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from unittest.mock import MagicMock

from db_manager import DBManager


class FakeDBConnection:
    """Тестовый двойник DBConnection с рабочим контекстным менеджером."""

    def __init__(self):
        self.mock_cur = MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    @property
    def conn(self):
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = self.mock_cur
        return mock_conn


class TestDBManager(unittest.TestCase):
    """Тесты методов чтения из БД."""

    def setUp(self):
        """Создаем фейковое соединение и DBManager."""
        self.fake_db = FakeDBConnection()
        self.mock_cur = self.fake_db.mock_cur
        self.manager = DBManager(self.fake_db)

    def test_get_countries_and_aeroplanes_count(self):
        """Получение списка стран с количеством самолетов."""
        self.mock_cur.fetchall.return_value = [("Germany", 15), ("Spain", 8)]
        result = self.manager.get_countries_and_aeroplanes_count()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ("Germany", 15))

    def test_get_all_aeroplanes(self):
        """Получение всех самолетов."""
        self.mock_cur.fetchall.return_value = [
            ("abc123", "UAL123", "United States", -5.0, 55.0, 10000, 200, False)
        ]
        result = self.manager.get_all_aeroplanes()
        self.assertEqual(len(result), 1)

    def test_get_avg_speed(self):
        """Получение средней скорости."""
        self.mock_cur.fetchone.return_value = [215.5]
        result = self.manager.get_avg_speed()
        self.assertAlmostEqual(result, 215.5)

    def test_get_avg_speed_none(self):
        """Нет данных -- средняя скорость None."""
        self.mock_cur.fetchone.return_value = [None]
        result = self.manager.get_avg_speed()
        self.assertIsNone(result)

    def test_get_aeroplanes_with_higher_speed(self):
        """Получение самолетов со скоростью выше средней."""
        self.mock_cur.fetchall.return_value = [
            ("abc123", "UAL123", "United States", 250.0)
        ]
        result = self.manager.get_aeroplanes_with_higher_speed()
        self.assertEqual(len(result), 1)

    def test_get_aeroplanes_with_keyword(self):
        """Поиск по позывному."""
        self.mock_cur.fetchall.return_value = [
            ("def456", "ACA456", "Canada", 250.0)
        ]
        result = self.manager.get_aeroplanes_with_keyword("ACA")
        self.assertEqual(len(result), 1)
        args = self.mock_cur.execute.call_args[0][1]
        self.assertIn("ACA", args[0])

    def test_get_aeroplanes_with_keyword_empty(self):
        """Поиск по позывному -- ничего не найдено."""
        self.mock_cur.fetchall.return_value = []
        result = self.manager.get_aeroplanes_with_keyword("ZZZ")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
