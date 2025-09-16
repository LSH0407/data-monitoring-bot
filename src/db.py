from typing import Dict, Any
import mysql.connector

def save_event(conn_info: Dict[str, str], table: str, payload: Dict[str, Any]) -> None:
    cnx = mysql.connector.connect(
        host=conn_info.get("host", "localhost"),
        user=conn_info.get("user"),
        password=conn_info.get("password"),
        database=conn_info.get("database"),
    )
    try:
        cols = ",".join(payload.keys())
        placeholders = ",".join(["%s"] * len(payload))
        sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        with cnx.cursor() as cur:
            cur.execute(sql, list(payload.values()))
        cnx.commit()
    finally:
        cnx.close()
