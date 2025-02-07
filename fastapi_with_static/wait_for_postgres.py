import time

import psycopg2

from src.core.app_settings import app_settings


def wait_for_postgres():
    while True:
        try:
            print(f"Connecting to PostgreSQL")
            conn = psycopg2.connect(
                host=app_settings.POSTGRES_HOST,
                port=app_settings.POSTGRES_PORT,
                user=app_settings.POSTGRES_USER,
                password=app_settings.POSTGRES_PASS,
                dbname=app_settings.POSTGRES_NAME
            )
            conn.close()
            print("PostgreSQL is ready!")
            break
        except psycopg2.OperationalError as e:
            print(f"Waiting for PostgreSQL to be ready... ({e})")
            time.sleep(1)


if __name__ == "__main__":
    wait_for_postgres()
