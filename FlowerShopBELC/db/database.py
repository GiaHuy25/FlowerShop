import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()  # Load biến môi trường từ .env

# Lấy chuỗi kết nối từ .env
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Trả về kết nối tới SQL Server"""
    try:
        conn = pyodbc.connect(DATABASE_URL)
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
        raise

def close_db_connection(conn):
    """Đóng kết nối database"""
    if conn:
        conn.close()