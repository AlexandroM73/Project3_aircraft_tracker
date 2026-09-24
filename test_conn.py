from src.db_config import DB_CONFIG
import psycopg2

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("✅ УСПЕШНОЕ ПОДКЛЮЧЕНИЕ К POSTGRESQL!")
    print(f"Версия сервера: {version}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ ОШИБКА ПОДКЛЮЧЕНИЯ: {e}")
    print("Проверь пароль в src/db_config.py!")
