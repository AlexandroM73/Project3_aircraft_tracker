# Aircraft Tracker (PostgreSQL)

Учебный проект: получение данных о самолетах в реальном времени через OpenSky Network API,
геоданные стран через Nominatim, хранение в PostgreSQL.

## Возможности

- Получение координат границ стран и самолетов в их воздушном пространстве.
- Хранение данных в PostgreSQL.
- Класс `DBManager` с методами:
  - `get_countries_and_aeroplanes_count()` -- страны и количество самолетов.
  - `get_all_aeroplanes()` -- все самолеты.
  - `get_avg_speed()` -- средняя скорость.
  - `get_aeroplanes_with_higher_speed()` -- быстрее среднего.
  - `get_aeroplanes_with_keyword("ACA")` -- поиск по позывному.

## SOLID

- **SRP**: `DBConnection` -- только соединение; `DBWriter` -- только запись; `DBManager` -- только чтение.
- **OCP**: `main.py` не зависит от конкретного API-класса, принимает любой `AbstractAPI`.
- **DIP**: `main.py` принимает `DBManager` и `DBWriter` через их интерфейсы.

## Установка и запуск

```bash
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\\Scripts\\activate       # Windows

pip install -r requirements.txt

psql -U postgres -c "CREATE DATABASE aircraft_tracker;"
psql -U postgres -d aircraft_tracker -f sql/schema.sql

# Настроить доступ в src/db_config.py

python main.py
```

## Тесты

```bash
python -m unittest discover -s test -v
```

## Покрытие

```bash
coverage run -m unittest discover -s test
coverage report
```
