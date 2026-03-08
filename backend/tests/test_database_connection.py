"""
Tests for DatabaseConnection class

WARNING: These tests run against the production database.
They use a dedicated test_records table to avoid interfering with real data.
"""
import pytest
import logging
from data.database.connection import DatabaseConnection


logger = logging.getLogger(__name__)


class TestDatabaseConnection:
    """Test suite for DatabaseConnection class"""

    @pytest.fixture
    def setup_test_table(self, db_connection):
        """Create and cleanup test table before and after each test"""
        # Create test table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS test_records (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            value INTEGER
        )
        """
        db_connection.execute_query(create_table_sql)

        yield

        # Cleanup: Drop test table after test
        db_connection.execute_query("DROP TABLE IF EXISTS test_records")

    def test_connection_establishment(self, db_connection):
        """Test that we can establish a database connection"""
        with db_connection.get_connection() as conn:
            assert conn is not None
            assert not conn.closed

        # Connection should be closed after context manager exits
        assert conn.closed

    def test_insert_record(self, db_connection, setup_test_table):
        """Test inserting a record into the database"""
        insert_sql = "INSERT INTO test_records (name, value) VALUES (%s, %s)"
        rows_affected = db_connection.execute_query(
            insert_sql,
            params=("test_item", 42)
        )

        assert rows_affected == 1

        # Verify the record was inserted
        result = db_connection.fetch_one(
            "SELECT name, value FROM test_records WHERE name = %s",
            params=("test_item",)
        )
        assert result is not None
        assert result[0] == "test_item"
        assert result[1] == 42

    def test_retrieve_record(self, db_connection, setup_test_table):
        """Test retrieving a record from the database"""
        # Insert a test record first
        db_connection.execute_query(
            "INSERT INTO test_records (name, value) VALUES (%s, %s)",
            params=("retrieve_test", 100)
        )

        # Test fetch_one
        result = db_connection.fetch_one(
            "SELECT id, name, value FROM test_records WHERE name = %s",
            params=("retrieve_test",)
        )
        assert result is not None
        assert result[1] == "retrieve_test"
        assert result[2] == 100

        # Test fetch_results (multiple records)
        db_connection.execute_query(
            "INSERT INTO test_records (name, value) VALUES (%s, %s)",
            params=("retrieve_test_2", 200)
        )
        results = db_connection.fetch_results(
            "SELECT name, value FROM test_records ORDER BY value"
        )
        assert len(results) == 2
        assert results[0][0] == "retrieve_test"
        assert results[1][0] == "retrieve_test_2"

    def test_delete_record(self, db_connection, setup_test_table):
        """Test deleting a record from the database"""
        # Insert a test record
        db_connection.execute_query(
            "INSERT INTO test_records (name, value) VALUES (%s, %s)",
            params=("delete_test", 999)
        )

        # Verify it exists
        result = db_connection.fetch_one(
            "SELECT name FROM test_records WHERE name = %s",
            params=("delete_test",)
        )
        assert result is not None

        # Delete the record
        rows_affected = db_connection.execute_query(
            "DELETE FROM test_records WHERE name = %s",
            params=("delete_test",)
        )
        assert rows_affected == 1

        # Verify it's gone
        result = db_connection.fetch_one(
            "SELECT name FROM test_records WHERE name = %s",
            params=("delete_test",)
        )
        assert result is None

    def test_rollback_on_error(self, db_connection, setup_test_table):
        """Test that transactions are rolled back on error"""
        # Insert a valid record
        db_connection.execute_query(
            "INSERT INTO test_records (name, value) VALUES (%s, %s)",
            params=("before_error", 1)
        )

        # Count records before error
        count_before = db_connection.fetch_one(
            "SELECT COUNT(*) FROM test_records"
        )[0]

        # Try to execute a query that will fail within a transaction
        with pytest.raises(Exception):
            with db_connection.get_connection() as conn:
                cursor = conn.cursor()
                # First insert should happen
                cursor.execute(
                    "INSERT INTO test_records (name, value) VALUES (%s, %s)",
                    ("should_rollback", 2)
                )
                # This should cause an error (invalid SQL)
                cursor.execute("INVALID SQL STATEMENT")

        # Count records after error - should be same as before
        # because the transaction was rolled back
        count_after = db_connection.fetch_one(
            "SELECT COUNT(*) FROM test_records"
        )[0]

        assert count_after == count_before

        # Verify the rolled-back record doesn't exist
        result = db_connection.fetch_one(
            "SELECT name FROM test_records WHERE name = %s",
            params=("should_rollback",)
        )
        assert result is None

    def test_execute_many(self, db_connection, setup_test_table):
        """Test executing multiple inserts with execute_many"""
        insert_sql = "INSERT INTO test_records (name, value) VALUES (%s, %s)"
        params_list = [
            ("item_1", 10),
            ("item_2", 20),
            ("item_3", 30)
        ]

        rows_affected = db_connection.execute_many(insert_sql, params_list)
        assert rows_affected == 3

        # Verify all records were inserted
        results = db_connection.fetch_results(
            "SELECT name, value FROM test_records ORDER BY value"
        )
        assert len(results) == 3
        assert results[0][0] == "item_1"
        assert results[1][0] == "item_2"
        assert results[2][0] == "item_3"

    def test_cursor_context_manager(self, db_connection, setup_test_table):
        """Test that cursor context manager works correctly"""
        with db_connection.get_cursor() as cursor:
            assert cursor is not None
            cursor.execute(
                "INSERT INTO test_records (name, value) VALUES (%s, %s)",
                ("cursor_test", 123)
            )

        # Verify the insert was committed
        result = db_connection.fetch_one(
            "SELECT value FROM test_records WHERE name = %s",
            params=("cursor_test",)
        )
        assert result is not None
        assert result[0] == 123
