"""Database connection and raw SQL execution module.

Uses psycopg for PostgreSQL when available/configured, with automatic fallback
to SQLite for offline local demo runs so the app never fails on systems
without an active PostgreSQL service.

Both backends are abstracted behind two helpers:
- execute_query()  -> SELECT, returns list[dict]
- execute_commit() -> INSERT/UPDATE/DELETE, returns new id (INSERT) or rowcount
"""

import os
import sqlite3
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pink_wheels")

# Once a PostgreSQL connection attempt fails we keep using SQLite for the rest
# of the process lifetime. Retrying on every request would add a connect
# timeout to each API call during offline demos.
_pg_disabled = False


def _is_sqlite(conn) -> bool:
    """True when the given connection is a SQLite connection."""
    return isinstance(conn, sqlite3.Connection)


def get_db_connection():
    """Returns a database connection: PostgreSQL if reachable, else SQLite."""
    global _pg_disabled

    if not _pg_disabled and (
        DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")
    ):
        try:
            import psycopg
            from psycopg.rows import dict_row

            return psycopg.connect(DATABASE_URL, row_factory=dict_row, connect_timeout=2)
        except Exception:
            # PostgreSQL server not reachable locally; fall back to SQLite.
            _pg_disabled = True

    db_path = os.path.join(os.path.dirname(__file__), "pink_wheels_dsa.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _adapt_sql(query: str, sqlite: bool) -> str:
    """Translate DB-API placeholders and add a RETURNING clause for PG inserts."""
    if sqlite:
        return query.replace("%s", "?")
    return query


def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Execute a SELECT query and return rows as a list of dicts."""
    conn = get_db_connection()
    sqlite = _is_sqlite(conn)
    try:
        cur = conn.cursor()
        cur.execute(_adapt_sql(query, sqlite), params)
        rows = cur.fetchall()
        cur.close()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def execute_commit(query: str, params: tuple = ()) -> int:
    """Execute an INSERT/UPDATE/DELETE.

    Returns the generated id for INSERT statements and the affected row count
    for UPDATE/DELETE statements.
    """
    conn = get_db_connection()
    sqlite = _is_sqlite(conn)
    try:
        cur = conn.cursor()
        query = _adapt_sql(query, sqlite)
        is_insert = query.lstrip().upper().startswith("INSERT")

        if is_insert and not sqlite and "RETURNING" not in query.upper():
            query = query.rstrip().rstrip(";") + " RETURNING id"

        cur.execute(query, params)

        if is_insert:
            if sqlite:
                new_id = cur.lastrowid or 0
            else:
                row = cur.fetchone()
                if isinstance(row, dict):
                    new_id = row.get("id", 0)
                else:
                    new_id = row[0] if row else 0
            result = new_id
        else:
            result = max(cur.rowcount, 0) if cur.rowcount is not None else 0

        conn.commit()
        cur.close()
        return result
    finally:
        conn.close()


def database_engine() -> str:
    """Returns the active backend name: 'postgresql' or 'sqlite'."""
    conn = get_db_connection()
    try:
        return "sqlite" if _is_sqlite(conn) else "postgresql"
    finally:
        conn.close()


def init_db():
    """Initialize the passengers and rides tables and seed demo passengers."""
    conn = get_db_connection()
    sqlite = _is_sqlite(conn)
    try:
        cur = conn.cursor()

        if not sqlite:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS passengers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    phone VARCHAR(50) NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rides (
                    id SERIAL PRIMARY KEY,
                    passenger_id INTEGER,
                    driver_id INTEGER,
                    pickup_location TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    pickup_latitude DOUBLE PRECISION NOT NULL,
                    pickup_longitude DOUBLE PRECISION NOT NULL,
                    destination_latitude DOUBLE PRECISION NOT NULL,
                    destination_longitude DOUBLE PRECISION NOT NULL,
                    distance_km DOUBLE PRECISION DEFAULT 0.0,
                    fare DOUBLE PRECISION DEFAULT 0.0,
                    vehicle_type VARCHAR(50) DEFAULT 'Bike',
                    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        else:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS passengers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rides (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    passenger_id INTEGER,
                    driver_id INTEGER,
                    pickup_location TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    pickup_latitude REAL NOT NULL,
                    pickup_longitude REAL NOT NULL,
                    destination_latitude REAL NOT NULL,
                    destination_longitude REAL NOT NULL,
                    distance_km REAL DEFAULT 0.0,
                    fare REAL DEFAULT 0.0,
                    vehicle_type TEXT DEFAULT 'Bike',
                    status TEXT NOT NULL DEFAULT 'PENDING',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
            """)

        conn.commit()

        # Seed demo passengers only when the table is empty.
        cur.execute("SELECT COUNT(*) AS c FROM passengers")
        row = cur.fetchone()
        count = row["c"] if isinstance(row, dict) else row[0]
        if count == 0:
            placeholder = "?" if sqlite else "%s"
            seed = [
                ("Fatima Noor", "+92 300 1234567"),
                ("Ayesha Khan", "+92 321 7654321"),
                ("Zainab Ali", "+92 333 9876543"),
            ]
            cur.executemany(
                f"INSERT INTO passengers (name, phone) VALUES ({placeholder}, {placeholder})",
                seed,
            )
            conn.commit()

        cur.close()
    finally:
        conn.close()
