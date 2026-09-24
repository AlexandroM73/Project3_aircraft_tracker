"""Тесты для DBWriter (psycopg2 мокируется)."""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from unittest.mock import MagicMock

from db_writer import DBWriter


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


class TestDBWriter(unittest.TestCase):
    """Тесты методов записи в БД."""

    def setUp(self):
        """Создаем фейковое соединение и DBWriter."""
        self.fake_db = FakeDBConnection()
        self.mock_cur = self.fake_db.mock_cur
        self.writer = DBWriter(self.fake_db)

    def test_insert_country(self):
        """Вставка страны -- вызывается execute с правильными параметрами."""
        self.writer.insert_country("France", [51.0, 60.0, -10.0, 2.0])
        self.mock_cur.execute.assert_called_once()
        args = self.mock_cur.execute.call_args[0][1]
        self.assertEqual(args, ("France", 51.0, 60.0, -10.0, 2.0))

    def test_insert_aeroplanes(self):
        """Массовая вставка самолетов."""
        planes = [
            ["abc123", "UAL123", "United States", None, None,
             -5.0, 55.0, 10000, 200, 90, 0, False, "1234", False],
            ["def456", "ACA456", "Canada", None, None,
             -6.0, 56.0, 11000, 250, 85, 0, False, "5678", False],
        ]
        count = self.writer.insert_aeroplanes(planes)
        self.assertEqual(count, 2)
        self.mock_cur.executemany.assert_called_once()

    def test_insert_aeroplanes_empty(self):
        """Пустой список -- ничего не вставляется."""
        count = self.writer.insert_aeroplanes([])
        self.assertEqual(count, 0)
        self.mock_cur.executemany.assert_not_called()

    def test_clear_aeroplanes(self):
        """Очистка таблицы самолетов."""
        self.writer.clear_aeroplanes()
        self.mock_cur.execute.assert_called_once()
        sql = self.mock_cur.execute.call_args[0][0]
        self.assertIn("DELETE FROM aeroplanes", sql)


if __name__ == "__main__":
    unittest.main()
