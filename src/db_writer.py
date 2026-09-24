"""Запись данных в PostgreSQL (SRP: только запись/заполнение таблиц)."""

from db_connection import DBConnection


class DBWriter:
    """Класс для записи стран и самолетов в базу данных.

    Отвечает только за вставку и очистку данных.
    Чтение данных -- ответственность DBManager, что соответствует SRP.
    """

    def __init__(self, db_connection: DBConnection) -> None:
        """Инициализация с экземпляром DBConnection.

        Args:
            db_connection: Контекстный менеджер соединения с БД.
        """
        self._db = db_connection

    def insert_country(self, name: str, bbox: list[float]) -> None:
        """Вставить или обновить запись о стране.

        Args:
            name: Название страны.
            bbox: Список [min_lat, max_lat, min_lon, max_lon].
        """
        min_lat, max_lat, min_lon, max_lon = bbox
        query = """
            INSERT INTO countries (name, bbox_min_lat, bbox_max_lat, bbox_min_lon, bbox_max_lon)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE SET
                bbox_min_lat = EXCLUDED.bbox_min_lat,
                bbox_max_lat = EXCLUDED.bbox_max_lat,
                bbox_min_lon = EXCLUDED.bbox_min_lon,
                bbox_max_lon = EXCLUDED.bbox_max_lon
        """
        with self._db as dbc:
            cur = dbc.conn.cursor()
            cur.execute(query, (name, min_lat, max_lat, min_lon, max_lon))

    def insert_aeroplanes(self, planes_data: list[list]) -> int:
        """Вставить список самолетов в БД (массовая вставка).

        Args:
            planes_data: Список state vectors из OpenSky API.

        Returns:
            Количество вставленных записей.
        """
        if not planes_data:
            return 0

        query = """
            INSERT INTO aeroplanes
            (icao24, callsign, origin_country, time_position, last_position_time,
             longitude, latitude, baro_altitude, velocity, true_track,
             vertical_rate, on_ground, squawk, spi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (icao24) DO UPDATE SET
                callsign = EXCLUDED.callsign,
                origin_country = EXCLUDED.origin_country,
                longitude = EXCLUDED.longitude,
                latitude = EXCLUDED.latitude,
                baro_altitude = EXCLUDED.baro_altitude,
                velocity = EXCLUDED.velocity,
                true_track = EXCLUDED.true_track,
                on_ground = EXCLUDED.on_ground
        """
        rows = []
        for s in planes_data:
            rows.append((
                s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8],
                s[9], s[10], s[11], s[12], s[13],
            ))

        with self._db as dbc:
            cur = dbc.conn.cursor()
            cur.executemany(query, rows)
        return len(rows)

    def clear_aeroplanes(self) -> None:
        """Очистить таблицу самолетов перед новой загрузкой данных."""
        with self._db as dbc:
            cur = dbc.conn.cursor()
            cur.execute("DELETE FROM aeroplanes")
