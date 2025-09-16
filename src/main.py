import socket, os
from typing import Optional, Tuple

class NaverWorksBot:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('NAVER_WORKS_TOKEN')

    def send_message(self, text: str) -> None:
        # 실제 API 키는 없다고 가정: 호출 부분은 스텁 처리
        print(f"[naverworks] {text}")


def detect_direct_feed(listen_ip: str = '0.0.0.0', port: int = 6000, timeout_sec: int = 10) -> bool:
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
    bot = NaverWorksBot()
    ok = detect_direct_feed()
    if ok:
        bot.send_message('수신용서버에서 직접 수신 감지됨')
    else:
        print('[monitor] no direct feed within timeout')

if __name__ == '__main__':
    main()
