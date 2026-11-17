import sqlite3
from pathlib import Path
import pandas as pd


def run_analytics(db_path: str, sql_path: str) -> None:
    sql_script = Path(sql_path).read_text(encoding="utf-8")
    # Trennt die einzelnen SQL-Abfragen anhand des Semikolons
    queries = [q.strip() for q in sql_script.split(";") if q.strip()]

    with sqlite3.connect(db_path) as conn:
        for i, query in enumerate(queries, start=1):
            print(f"\n--- Auswertung {i} ---")
            df = pd.read_sql_query(query, conn)
            print(df.to_string(index=False))


if __name__ == "__main__":
    run_analytics("data/processed/logistics.db", "src/queries.sql")