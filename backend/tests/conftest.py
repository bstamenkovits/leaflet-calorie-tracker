"""
Shared fixtures for tests
"""
import pytest
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / "src" / ".env"
load_dotenv(env_path)


@pytest.fixture(scope="session")
def db_connection():
    """Provide a DatabaseConnection instance for tests"""
    from data.database.connection import DatabaseConnection
    return DatabaseConnection()
