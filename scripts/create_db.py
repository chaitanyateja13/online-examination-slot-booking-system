import pymysql
import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

db_name = env('DB_NAME', default='exam_system_db')
db_user = env('DB_USER', default='root')
db_password = env('DB_PASSWORD', default='')
db_host = env('DB_HOST', default='127.0.0.1')
db_port = env('DB_PORT', default=3306)

try:
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, port=int(db_port))
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"Database {db_name} created or already exists.")
except Exception as e:
    print(f"Error creating database: {e}")
finally:
    if 'connection' in locals() and connection.open:
        cursor.close()
        connection.close()
