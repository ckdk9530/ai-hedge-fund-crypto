import os
import re
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

from src.utils.database import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DEFAULT_DSN

load_dotenv(find_dotenv())

SCHEMA_PATH = Path("init.sql")


def parse_schema(schema_path: Path):
    schema = {}
    pattern = re.compile(r"CREATE TABLE IF NOT EXISTS (\w+) \((.*?)\);", re.S)
    text = schema_path.read_text()
    for match in pattern.finditer(text):
        table = match.group(1)
        body = match.group(2)
        columns = []
        for line in body.splitlines():
            line = line.strip().rstrip(',')
            if not line or line.upper().startswith("FOREIGN KEY"):
                continue
            col_name = line.split()[0]
            columns.append((col_name, line))
        schema[table] = {"create": match.group(0), "columns": columns}
    return schema


def ensure_schema(conn, schema):
    with conn.cursor() as cur:
        for table, info in schema.items():
            cur.execute("SELECT to_regclass(%s)", (table,))
            exists = cur.fetchone()[0] is not None
            if not exists:
                print(f"Creating table {table}")
                cur.execute(info["create"])
                continue
            cur.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name=%s",
                (table,),
            )
            existing = {row[0] for row in cur.fetchall()}
            for col_name, definition in info["columns"]:
                if col_name not in existing:
                    print(f"Adding column {col_name} to {table}")
                    cur.execute(f"ALTER TABLE {table} ADD COLUMN {definition}")
        conn.commit()


def main():
    dsn = DEFAULT_DSN
    print(f"Connecting to {dsn}")
    conn = psycopg2.connect(dsn, cursor_factory=RealDictCursor)
    schema = parse_schema(SCHEMA_PATH)
    ensure_schema(conn, schema)
    conn.close()
    print("Database check complete.")


if __name__ == "__main__":
    main()
