import os
import mysql.connector
from typing import Any


class BaseDAO:
    def __init__(self):
        self.host = os.getenv('MYSQL_HOSTS')
        self.user = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASSWORD')
        self.database = os.getenv('MYSQL_DATABASE')

    def get_db_connection(self):
        return mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)

    def execute(self, query: str, params: tuple = (), commit: bool = False) -> None:
        conn = self.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            if commit:
                conn.commit()
        finally:
            cursor.close()
            conn.close()

    def fetch_one(self, query: str, params: tuple = ()) -> dict[str, Any] | None:
        conn = self.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            return row
        finally:
            cursor.close()
            conn.close()

    def fetch_all(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        conn = self.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return rows
        finally:
            cursor.close()
            conn.close()
