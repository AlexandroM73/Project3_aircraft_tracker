"""Точка входа: консольное меню для работы с трекером самолетов.

main.py не зависит от конкретного API-класса -- он принимает любой AbstractAPI.
Создание объектов вынесено в отдельную функцию, что упрощает тестирование
и замену реализации (DIP из SOLID).
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from abstract_api import AbstractAPI
from db_connection import DBConnection
from db_manager import DBManager
from db_writer import DBWriter
from db_config import COUNTRIES
import utils


def fetch_and_store(api: AbstractAPI, writer: DBWriter) -> int:
    """Получить данные о самолетах через API и записать в БД.

    Args:
        api: Экземпляр AbstractAPI (любая реализация).
        writer: Экземпляр DBWriter для записи в БД.

    Returns:
        Общее количество записанных самолетов.
    """
    total = 0
    writer.clear_aeroplanes()

    for country in COUNTRIES:
        print(f"\nЗапрос данных для: {country}...")
        bbox = api.get_country_bbox(country)
        if not bbox:
            print(f"Не удалось получить границы для {country}, пропуск.")
            continue

        writer.insert_country(country, bbox)
        planes = api.get_aeroplanes_in_bbox(*bbox)
        count = writer.insert_aeroplanes(planes)
        total += count
        print(f"  {country}: {count} самолетов")

    return total


def user_interaction(manager: DBManager) -> None:
    """Интерактивное меню для запросов к БД.

    Args:
        manager: Экземпляр DBManager для чтения данных.
    """
    while True:
        print("=" * 50)
        print("1 -- Страны и количество самолетов")
        print("2 -- Все самолеты")
        print("3 -- Средняя скорость")
        print("4 -- Самолеты быстрее среднего")
        print("5 -- Поиск по позывному")
        print("0 -- Выход")
        print("=" * 50)

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            data = manager.get_countries_and_aeroplanes_count()
            utils.print_countries_count(data)
        elif choice == "2":
            data = manager.get_all_aeroplanes()
            utils.print_aeroplanes(data)
        elif choice == "3":
            speed = manager.get_avg_speed()
            utils.print_avg_speed(speed)
        elif choice == "4":
            data = manager.get_aeroplanes_with_higher_speed()
            utils.print_higher_speed(data)
        elif choice == "5":
            keyword = input("Введите символы для поиска: ").strip()
            if keyword:
                data = manager.get_aeroplanes_with_keyword(keyword)
                utils.print_keyword_search(data, keyword)
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неверный выбор, попробуйте снова.\n")


def _create_api() -> AbstractAPI:
    """Фабричный метод для создания API-адаптера.

    Изолирует создание конкретного класса, что упрощает замену реализации (OCP).
    """
    from api_adapter import APIAdapter
    return APIAdapter()


def main() -> None:
    """Главная функция: создает объекты (DIP) и запускает процесс."""
    api = _create_api()
    db = DBConnection()

    writer = DBWriter(db)
    manager = DBManager(db)

    print("Загрузка данных о самолетах...")
    total = fetch_and_store(api, writer)
    print(f"\nВсего загружено: {total} самолетов\n")

    user_interaction(manager)


if __name__ == "__main__":
    main()
