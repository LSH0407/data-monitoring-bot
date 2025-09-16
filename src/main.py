import os
import socket
from typing import Optional, Dict, List
from .holidays import get_holidays
from .snmp import collect_status
from .db import save_event

CONFIG_DEFAULTS: Dict[str, str] = {
    "listen_ip": "0.0.0.0",
    "port": "6000",
    "timeout_sec": "10",
    # SNMP
    "snmp_host": "",
    "snmp_community": "public",
    "snmp_oids": "",  # comma separated
    # DB
    "db_host": "",
    "db_user": "",
    "db_password": "",
    "db_database": "",
    "db_table": "events",
    # Holidays
    "holiday_api": "",
    "holiday_crawl": "",
}


def load_config(exchange_name: str) -> Dict[str, str]:
    path = f"{exchange_name}.config"
    values: Dict[str, str] = dict(CONFIG_DEFAULTS)
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = [x.strip() for x in line.split("=", 1)]
                if k in values:
                    values[k] = v
    except FileNotFoundError:
        pass
    return values


def detect_direct_feed(listen_ip: str, port: int, timeout_sec: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, port))
    sock.settimeout(timeout_sec)
    try:
        _data, _addr = sock.recvfrom(2048)
        return True
    except socket.timeout:
        return False
    finally:
        sock.close()


def main() -> None:
    ex = os.getenv("EXCHANGE", "NASDAQ")
    cfg = load_config(ex)

    # Holiday check (optional): skip detection on holiday
    holidays = get_holidays(ex, cfg.get("holiday_api") or None, cfg.get("holiday_crawl") or None)

    # Direct feed detection
    ok = detect_direct_feed(cfg["listen_ip"], int(cfg["port"]), int(cfg["timeout_sec"]))

    # Optional SNMP polling
    snmp_data: Dict[str, str] = {}
    if cfg.get("snmp_host") and cfg.get("snmp_oids"):
        oids: List[str] = [s.strip() for s in cfg["snmp_oids"].split(",") if s.strip()]
        snmp_data = collect_status(cfg["snmp_host"], cfg["snmp_community"], oids)

    # Optional DB write
    if cfg.get("db_host") and cfg.get("db_user") and cfg.get("db_database"):
        event = {
            "exchange": ex,
            "detected": int(ok),
            "listen_ip": cfg["listen_ip"],
            "port": int(cfg["port"]),
            "holiday_count": len(holidays),
        }
        # flatten a few snmp values
        for i, (k, v) in enumerate(list(snmp_data.items())[:5]):
            event[f"snmp_{i}"] = f"{k}:{v}"
        save_event(
            {
                "host": cfg["db_host"],
                "user": cfg["db_user"],
                "password": cfg["db_password"],
                "database": cfg["db_database"],
            },
            cfg.get("db_table", "events"),
            event,
        )

    # Console summary
    print({
        "exchange": ex,
        "detected": ok,
        "snmp": bool(snmp_data),
        "holidays": len(holidays),
    })

if __name__ == "__main__":
    main()
