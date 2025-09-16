import socket, os, pathlib
from typing import Optional, Dict

CONFIG_KEYS = {
    'listen_ip': '0.0.0.0',
    'port': '6000',
    'timeout_sec': '10',
}

def load_config(exchange_name: str) -> Dict[str, str]:
    filename = f"{exchange_name}.config"
    p = pathlib.Path(filename)
    if not p.exists():
        raise FileNotFoundError(f"config not found: {filename}")
    values: Dict[str, str] = dict(CONFIG_KEYS)
    for line in p.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip()
        if k in CONFIG_KEYS:
            values[k] = v
    return values

class NaverWorksBot:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('NAVER_WORKS_TOKEN')

    def send_message(self, text: str) -> None:
        # 실제 API 키는 없다고 가정: 호출 부분은 스텁 처리
        print(f"[naverworks] {text}")


def detect_direct_feed(listen_ip: str, port: int, timeout_sec: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_ip, port))
    sock.settimeout(timeout_sec)
    try:
        data, addr = sock.recvfrom(2048)
        print(f"[monitor] received {len(data)} bytes from {addr}")
        return True
    except socket.timeout:
        return False
    finally:
        sock.close()


def main() -> None:
    exchange = os.getenv('EXCHANGE', 'NASDAQ')
    cfg = load_config(exchange)
    listen_ip = cfg['listen_ip']
    port = int(cfg['port'])
    timeout_sec = int(cfg['timeout_sec'])

    bot = NaverWorksBot()
    ok = detect_direct_feed(listen_ip, port, timeout_sec)
    if ok:
        bot.send_message(f"[{exchange}] 수신용서버에서 직접 수신 감지됨")
    else:
        print(f"[monitor] [{exchange}] no direct feed within {timeout_sec}s")

if __name__ == '__main__':
    main()
