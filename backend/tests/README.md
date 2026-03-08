# Backend Tests

Simple testing setup using pytest for the leaflet-calorie-tracker backend.

## Setup

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure your `.env` file has the database connection details set up.

## Running Tests

From the `backend` directory, run:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_database_connection.py

# Run specific test
pytest tests/test_database_connection.py::TestDatabaseConnection::test_insert_record
```

## Test Structure

- `conftest.py` - Shared fixtures and configuration
- `test_database_connection.py` - Tests for the DatabaseConnection class

## Important Notes

* **WARNING**: Tests run against the production database. They use a dedicated `test_records` table that is created and dropped for each test to minimize impact on production data.
* **NOTE**: The database connection is established using connection parameters defined in a `.env` file assumed to be located in the `backend/src/` directory. As a result the tests only work locally, so no CI testing for this hobby project. 
