from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy import inspect
from sqlalchemy import text
from core.database import engine, Base
from sqlalchemy.exc import OperationalError

# List of columns you want to ensure exist
required_columns = {
    "description": "TEXT",
    "base_score": "FLOAT",
    "identifier": "TEXT",
    "status": "TEXT",
    "metrics": "TEXT",
    "configurations": "TEXT"
}

with engine.connect() as conn:
    inspector = inspect(engine)
    existing_columns = [col['name'] for col in inspector.get_columns('cves')]

    for col_name, col_type in required_columns.items():
        if col_name not in existing_columns:
            print(f"Adding column '{col_name}'")
            try:
                conn.execute(text(f'ALTER TABLE cves ADD COLUMN {col_name} {col_type}'))
            except Exception as e:
                print(f"Could not add column '{col_name}': {e}")

print("Migration completed.")
