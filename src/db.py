from typing import Dict, Any
import mysql.connector


def ensure_table(conn_info: Dict[str, str], table: str) -> None:
    cnx = mysql.connector.connect(
        host=conn_info.get("host", "localhost"),
        user=conn_info.get("user"),
        password=conn_info.get("password"),
        database=conn_info.get("database"),
    )
    try:
        ddl = f"""
        CREATE TABLE IF NOT EXISTS `{table}` (
          id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
          ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          exchange VARCHAR(32) NOT NULL,
          detected TINYINT(1) NOT NULL,
          listen_ip VARCHAR(64) NULL,
          port INT NULL,
          holiday_count INT NULL,
          snmp_0 VARCHAR(255) NULL,
          snmp_1 VARCHAR(255) NULL,
          snmp_2 VARCHAR(255) NULL,
          snmp_3 VARCHAR(255) NULL,
          snmp_4 VARCHAR(255) NULL,
          PRIMARY KEY (id),
          KEY idx_ts (ts),
          KEY idx_exchange (exchange)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        with cnx.cursor() as cur:
            cur.execute(ddl)
        cnx.commit()
    finally:
        cnx.close()


def save_event(conn_info: Dict[str, str], table: str, payload: Dict[str, Any]) -> None:
    cnx = mysql.connector.connect(
        host=conn_info.get("host", "localhost"),
        user=conn_info.get("user"),
        password=conn_info.get("password"),
        database=conn_info.get("database"),
    )
    try:
        cols = ",".join([f"`{c}`" for c in payload.keys()])
        placeholders = ",".join(["%s"] * len(payload))
        sql = f"INSERT INTO `{table}` ({cols}) VALUES ({placeholders})"
        with cnx.cursor() as cur:
            cur.execute(sql, list(payload.values()))
        cnx.commit()
    finally:
        cnx.close()
