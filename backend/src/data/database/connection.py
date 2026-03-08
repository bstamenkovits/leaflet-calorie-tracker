import psycopg2
import os
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Any


logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    A class to manage PostgreSQL database connections and operations.
    """

    def __init__(self):
        """Initialize SQLite database connection."""
        pass

    @contextmanager
    def get_connection(self):
        """Context manager for database connections with auto-commit"""
        connection = None
        try:
            connection = psycopg2.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME")
            )
            logger.info("Database connection established")
            yield connection
            connection.commit()  # Auto-commit on successful operations
        except Exception as e:
            logger.error(f"Database error: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()

    @contextmanager
    def get_cursor(self) -> Generator[Any, None, None]:
        """Context manager for database connections"""
        with self.get_connection() as conn:
            yield conn.cursor()

    def execute_query(self, query: str, params=None):
        """
        Execute a query that modifies the database (INSERT, UPDATE, DELETE)

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to bind to the query.

        Returns:
            (int): Number of affected rows.

        Example:
            ```python
            db = DatabaseConnection("mydb.db")
            db.execute_query(
                query="INSERT INTO users (name, age) VALUES (?, ?)",
                params=("Alice", 30)
            )
            ```
        """
        with self.get_cursor() as cursor:
            logging.debug(f"Executing query: {query} with params: {params}")
            cursor.execute(query, params or [])
            return cursor.rowcount

    def execute_many(self, query: str, params_list):
        """
        Execute a query multiple times with different parameters

        Args:
            query (str): The SQL query to execute.
            params_list (list of tuple): List of parameter tuples to bind to the query.

        Returns:
            (int): Number of affected rows.

        Example:
            ```python
            db = DatabaseConnection("mydb.db")
            db.execute_many(
                query="INSERT INTO users (name, age) VALUES (?, ?)",
                params_list=[
                    ("Alice", 30),
                    ("Bob", 25),
                    ("Charlie", 35)
                ]
            )
            ```
        """
        with self.get_cursor() as cursor:
            logging.debug(f"Executing query: {query} with params_list: {params_list}")
            cursor.executemany(query, params_list)
            return cursor.rowcount

    def fetch_results(self, query: str, params=None):
        """Fetch all results from a SELECT query"""
        with self.get_cursor() as cursor:
            logging.debug(f"Fetching results for query: {query} with params: {params}")
            cursor.execute(query, params or [])
            return cursor.fetchall()

    def fetch_one(self, query: str, params=None):
        """Fetch a single result from a SELECT query"""
        with self.get_cursor() as cursor:
            logging.debug(f"Fetching single result for query: {query} with params: {params}")
            cursor.execute(query, params or [])
            return cursor.fetchone()
