"""Управление соединением с PostgreSQL (SRP: только подключение/отключение)."""

from db_config import DB_CONFIG


class DBConnection:
    """Контекстный менеджер для управления соединением с PostgreSQL.

    Открывает соединение при входе в блок with, закрывает при выходе.
    Единственная ответственность класса -- управление жизненным циклом соединения.
    """

    def __init__(self, config: dict | None = None):
        """Инициализация с конфигурацией БД.

        Args:
            config: Словарь с параметрами подключения.
                    Если None -- используется DB_CONFIG из db_config.py.
        """
        self._config = config or DB_CONFIG
        self._conn = None

    @property
    def conn(self):
        """Возвращает активное соединение или поднимает RuntimeError."""
        if self._conn is None or self._conn.closed:
            raise RuntimeError("Соединение не открыто. Используйте контекстный менеджер.")
        return self._conn

    def __enter__(self) -> "DBConnection":
        """Открывает соединение при входе в with.

        Ленивый импорт psycopg2 позволяет тестам работать без установленной библиотеки.
        """
        import psycopg2
        self._conn = psycopg2.connect(**self._config)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Закрывает соединение при выходе из with."""
        if self._conn is not None:
            if exc_type is not None:
                self._conn.rollback()
            else:
                self._conn.commit()
            self._conn.close()
            self._conn = None
