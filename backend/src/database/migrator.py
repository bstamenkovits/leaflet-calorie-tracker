import hashlib
import logging
from pathlib import Path
from database.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class SQLMigrator:
    def __init__(self):
        self.db = DatabaseConnection()
        self.migrations = Path(__file__).parent / "migrations"
        self._ensure_migration_table()

    @staticmethod
    def get_file_hash(filepath: Path) -> str:
        """Get md5 hash of SQL file to detect changes"""
        return hashlib.md5(filepath.read_text().encode()).hexdigest()

    def _ensure_migration_table(self):
        """
        Private method to make sure the `_migrations` table exists to track
        applied migrations. If it does not exist, it will be created.
        """
        query = """
            CREATE TABLE IF NOT EXISTS _migrations (
                file_name TEXT PRIMARY KEY,
                file_hash TEXT NOT NULL,
                applied_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.db.execute_query(query=query)

    def apply_migration(self, query, file_name, current_hash: str):
        """
        Apply a single migration and record it in the _migrations table.

        Args:
            query (str): The SQL query to execute.
            file_name (str): The name of the migration file.
            current_hash (str): The hash of the migration file content.

        Raises:
            Exception: If the migration fails to apply.

        Returns:
            None

        Example:
            ```python
            migrator = SQLMigrator()
            migrator.apply_migration(
                query="CREATE TABLE test (id SERIAL PRIMARY KEY)",
                file_name="001_create_test_table.sql",
                current_hash="abc123"
            )
            ```
        """
        with self.db.get_cursor() as cursor:
            try:
                cursor.execute(query)
                cursor.execute(
                    """
                        INSERT INTO _migrations (file_name, file_hash)
                        VALUES (%s, %s)
                        ON CONFLICT (file_name) DO NOTHING
                    """,
                    (file_name, current_hash)
                )
            except Exception:
                cursor.connection.rollback()
                raise

    def run_migrations(self):
        """
        Auto-apply SQL schema files

        This method will scan the migrations directory (located in the same
        directory as this script) for .sql files. For each file it will determine
        if the migration has already been applied by checking the _migrations table.
        If the migration is new, it will be applied and recorded in the database.
        If a migration has been applied but the file content has changed
        (detected via hash), an error will be raised to prevent unintended
        schema changes.

        Raises:
            Exception: If a migration fails to apply or if a previously applied migration has changed.

        Returns:
            None

        Example:
            ```python
            migrator = SQLMigrator()
            migrator.run_migrations()
            ```
        """
        logger.info("Starting SQL migrations...")
        for sql_file in sorted(self.migrations.glob("*.sql")):
            logger.info(f"Processing migration: {sql_file.name}")
            current_hash = self.get_file_hash(sql_file)
            file_name = sql_file.name

            # check if already applied
            result = self.db.fetch_results(
                query="SELECT file_hash FROM _migrations WHERE file_name = %s",
                params=(file_name,)
            )

            # TODO: implement forward-only migrations with version numbers
            if len(result) == 0:
                logger.info(f"Migration {file_name} not found in database. Applying new migration.")
                query = sql_file.read_text()
                try:
                    self.apply_migration(query, file_name, current_hash)
                except Exception as e:
                    logger.exception(f"Failed to apply migration {file_name}")
                    raise
                logger.info(f"✓ Successfully applied: {file_name}")

            elif result[0]['file_hash'] != current_hash:
                logger.error(error_msg := f"Migration {file_name} has changed since it was last applied. Detected hash: {current_hash}, expected hash: {result[0]['file_hash']}.")
                raise Exception(error_msg)

            else:
                logger.info(f"⊘ Skipped (unchanged): {file_name}")
