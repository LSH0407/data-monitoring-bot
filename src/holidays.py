from typing import Set, Optional
import requests
from bs4 import BeautifulSoup

def get_holidays(exchange: str, api_url: Optional[str] = None, crawl_url: Optional[str] = None) -> Set[str]:
    days: Set[str] = set()
    try:
        if api_url:
            r = requests.get(api_url, timeout=5)
            r.raise_for_status()
            data = r.json()
            for d in data.get("holidays", []):
                days.add(str(d))
        elif crawl_url:
            r = requests.get(crawl_url, timeout=5)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for el in soup.select("[data-date], time[datetime]"):
                days.add(el.get("data-date") or el.get("datetime"))
    except Exception:
        pass
    return days
