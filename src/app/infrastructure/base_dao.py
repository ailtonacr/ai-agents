import os
import mysql.connector
from typing import Any
from .logging_config import logger


class BaseDAO:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOSTS")
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DATABASE")

    def get_db_connection(self):
        try:
            conn = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password, database=self.database
            )
            return conn
        except Exception as e:
            logger.error(f"Failed to establish database connection: {str(e)}")
            raise

    def execute(self, query: str, params: tuple = (), commit: bool = False) -> None:
        conn = self.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            if commit:
                conn.commit()
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
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
        except Exception as e:
            logger.error(f"Fetch one failed: {str(e)}")
            raise
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
        except Exception as e:
            logger.error(f"Fetch all failed: {str(e)}")
            raise
        finally:
            cursor.close()
            conn.close()
