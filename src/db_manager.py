"""Чтение данных из PostgreSQL (SRP: только запросы на чтение)."""

from db_connection import DBConnection


class DBManager:
    """Класс для выполнения запросов к БД на чтение.

    Отвечает только за извлечение данных и аналитику.
    Запись данных -- ответственность DBWriter, что соответствует SRP.
    """

    def __init__(self, db_connection: DBConnection) -> None:
        """Инициализация с экземпляром DBConnection.

        Args:
            db_connection: Контекстный менеджер соединения с БД.
        """
        self._db = db_connection

    def get_countries_and_aeroplanes_count(self) -> list[tuple]:
        """Получить список всех стран и количество самолетов в их воздушном пространстве.

        Returns:
            Список кортежей (country_name, aeroplane_count).
        """
        query = """
            SELECT c.name, COUNT(a.icao24) AS count
            FROM countries c
            LEFT JOIN aeroplanes a ON a.origin_country = c.name
            GROUP BY c.name
            ORDER BY count DESC
        """
        with self._db as dbc:
            cur = dbc.conn.cursor()
            cur.execute(query)
            return cur.fetchall()

    def get_all_aeroplanes(self) -> list[tuple]:
        """Получить список всех воздушных судов из БД.

        Returns:
            Список кортежей с данными о каждом самолете.
        """
        query = """
            SELECT icao24, callsign, origin_country, longitude, latitude,
                   baro_altitude, velocity, on_ground
            FROM aeroplanes
            ORDER BY callsign
        """
        with self._db as dbc:
            cur = dbc.conn.cursor()
            cur.execute(query)
            return cur.fetchall()

    def get_avg_speed(self) -> float | None:
        """Получить среднюю скорость всех самолетов.

        Returns:
            Среднее значение скорости (м/с) или None, если данных нет.
        """
        query = "SELECT AVG(velocity) FROM aeroplanes WHERE velocity IS NOT NULL"
        with self._db as dbc:
            cur = dbc.conn.cursor()
            cur.execute(query)
            result = cur.fetchone()
            return result[0] if result else None

    def get_aeroplanes_with_higher_speed(self) -> list[tuple]:
        """Получить список самолетов, скорость которых выше средней.

        Returns:
            Список кортежей с самолетами, скорость которых выше среднего значения.
        """
        query = """
            SELECT icao24, callsign, origin_country, velocity
            FROM aeroplanes
            WHERE velocity > (SELECT AVG(velocity) FROM aeroplanes WHERE velocity IS NOT NULL)
            ORDER BY velocity DESC
        """
        with self._db as dbc:
            cur = dbc.conn.cursor()
            cur.execute(query)
            return cur.fetchall()

    def get_aeroplanes_with_keyword(self, keyword: str) -> list[tuple]:
        """Получить список самолетов, в позывном которых содержатся переданные символы.

        Args:
            keyword: Строка для поиска в позывном (например, ACA для Air Canada).

        Returns:
            Список кортежей с самолетами, позывной которых содержит keyword.
        """
        query = """
            SELECT icao24, callsign, origin_country, velocity
            FROM aeroplanes
            WHERE callsign ILIKE %s
            ORDER BY callsign
        """
        with self._db as dbc:
            cur = dbc.conn.cursor()
            cur.execute(query, (f"%{keyword}%",))
            return cur.fetchall()
