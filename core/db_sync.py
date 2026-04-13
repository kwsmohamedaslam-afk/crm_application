from sqlalchemy import inspect, text
from core.database import engine, Base


def sync_db():
    inspector = inspect(engine)

    for table_name, table in Base.metadata.tables.items():

        # If table doesn't exist → create it
        if table_name not in inspector.get_table_names():
            table.create(engine)
            print(f"✅ Created table: {table_name}")
            continue

        # Get existing columns
        existing_columns = [col["name"] for col in inspector.get_columns(table_name)]

        # Add missing columns
        for column in table.columns:
            if column.name not in existing_columns:
                col_type = column.type.compile(engine.dialect)
                nullable = "NULL" if column.nullable else "NOT NULL"

                query = f"""
                ALTER TABLE {table_name}
                ADD COLUMN {column.name} {col_type} {nullable}
                """

                with engine.connect() as conn:
                    conn.execute(text(query))
                    conn.commit()

                print(f"✅ Added column '{column.name}' to '{table_name}'")