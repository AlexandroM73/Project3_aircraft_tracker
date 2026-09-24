"""Конфигурация подключения к PostgreSQL и список отслеживаемых стран."""

DB_CONFIG = {
    "dbname": "aircraft_tracker",
    "user": "postgres",
    "password": "1",
    "host": "localhost",
    "port": 5432,
}

# Страны для отслеживания (минимум 4, взяли 5)
COUNTRIES = ["Germany", "Spain", "Canada", "Japan", "France"]
