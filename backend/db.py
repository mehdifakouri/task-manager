import os
import psycopg
from dotenv import load_dotenv


load_dotenv()
#تلاش برای اتصال

try:
    conn = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="task_manager",
        user="postgres",
        password= os.getenv("DB_PASSWORD")
    )
    print("connected to postgreSQL successfully")
    conn.close()
except Exception as e:
    print("connection failed:", e)

