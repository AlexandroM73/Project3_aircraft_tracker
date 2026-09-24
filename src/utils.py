"""Утилиты для форматированного вывода данных в консоль."""


def print_countries_count(data: list[tuple]) -> None:
    """Вывести таблицу стран и количества самолетов.

    Args:
        data: Список кортежей (country_name, aeroplane_count).
    """
    if not data:
        print("Нет данных о странах.")
        return
    print(f"{'Страна':<20} | {'Самолетов':>10}")
    print("-" * 34)
    for row in data:
        print(f"{row[0]:<20} | {row[1]:>10}")
    print()


def print_aeroplanes(data: list[tuple]) -> None:
    """Вывести список самолетов в человекочитаемом формате.

    Args:
        data: Список кортежей с данными о самолетах.
    """
    if not data:
        print("Нет данных о самолетах.")
        return
    print(f"{'ICAO24':<8} | {'Позывной':<10} | {'Страна':<18} | {'Скор.м/с':>9}")
    print("-" * 52)
    for row in data:
        icao = row[0] or ""
        callsign = row[1] or ""
        country = row[2] or ""
        vel = row[6] if len(row) > 6 and isinstance(row[6], (int, float)) else None
        vel_str = f"{vel:.2f}" if vel is not None else "---"
        print(f"{icao:<8} | {callsign:<10} | {country:<18} | {vel_str:>9}")
    print()


def print_avg_speed(speed: float | None) -> None:
    """Вывести среднюю скорость самолетов.

    Args:
        speed: Среднее значение скорости (м/с) или None.
    """
    if speed is None:
        print("Нет данных для расчета средней скорости.\n")
    else:
        print(f"Средняя скорость: {speed:.2f} м/с ({speed * 3.6:.2f} км/ч)\n")


def print_higher_speed(data: list[tuple]) -> None:
    """Вывести самолеты со скоростью выше средней.

    Args:
        data: Список кортежей (icao24, callsign, origin_country, velocity).
    """
    if not data:
        print("Нет самолетов со скоростью выше средней.\n")
        return
    print("Самолеты со скоростью выше средней:")
    print(f"{'ICAO24':<8} | {'Позывной':<10} | {'Страна':<18} | {'Скор.м/с':>9}")
    print("-" * 52)
    for row in data:
        icao = row[0] or ""
        callsign = row[1] or ""
        country = row[2] or ""
        vel = f"{row[3]:.2f}" if row[3] is not None else "---"
        print(f"{icao:<8} | {callsign:<10} | {country:<18} | {vel:>9}")
    print()


def print_keyword_search(data: list[tuple], keyword: str) -> None:
    """Вывести результаты поиска самолетов по позывному.

    Args:
        data: Список кортежей (icao24, callsign, origin_country, velocity).
        keyword: Ключевое слово для поиска.
    """
    if not data:
        print(f"Самолеты с позывным, содержащим \'{keyword}\', не найдены.\n")
        return
    print(f"Самолеты с позывным, содержащим \'{keyword}\' ({len(data)} шт.):")
    print(f"{'ICAO24':<8} | {'Позывной':<10} | {'Страна':<18} | {'Скор.м/с':>9}")
    print("-" * 52)
    for row in data:
        icao = row[0] or ""
        callsign = row[1] or ""
        country = row[2] or ""
        vel = f"{row[3]:.2f}" if row[3] is not None else "---"
        print(f"{icao:<8} | {callsign:<10} | {country:<18} | {vel:>9}")
    print()
