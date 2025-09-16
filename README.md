# 데이터 모니터링 알림봇\r\n\r\n수신용 서버에서 거래소별 직접 수신을 감지하고(UDP) 감지 시 네이버웍스 API 봇으로 알림을 보냅니다. 실제 API 키는 제공되지 않았으므로 알림 호출은 스텁으로 동작합니다.\r\n\r\n## 구성\r\n- 언어: Python 3.10+\r\n- 실행 엔트리: src/main.py (pyproject.toml의 monitor)\r\n- 설정 파일: 거래소명.config (예: NASDAQ.config)\r\n\r\n### 설정 형식(예: NASDAQ.config)\r\n`
\n# 예시 설정
\nlisten_ip=0.0.0.0\r\nport=6000\r\ntimeout_sec=10\r\n`
\n- listen_ip: 바인드 IP\r\n- port: 수신 포트\r\n- 	imeout_sec: 데이터 미수신 시 타임아웃(초)\r\n\r\n## 실행\r\n### 단일 거래소\r\n환경변수 EXCHANGE로 대상 거래소를 지정합니다.\r\n`
\nset EXCHANGE=NASDAQ
\npython -m src.main
\n`
\n\r\n### 여러 거래소 병렬 실행\r\n동봉 스크립트로 여러 프로세스를 띄울 수 있습니다.\r\n- PowerShell: un-multi.ps1 (기본 NASDAQ, NYSE, OPRA)
\n- 배치: un-multi.bat\r\n\r\n## 알림(스텁)
\n- NaverWorksBot.send_message()에서 실제 전송 대신 표준출력으로 대체\r\n\r\n## 개발 참고
\n- src/main.py는 거래소명.config를 읽어 수신 포트/타임아웃을 적용합니다.\r\n- 첫 패킷 수신 시 바로 감지/로그 출력 후 알림 스텁 호출\r\n


## 추가 설정 키
- snmp_host / snmp_community / snmp_oids (comma)
- db_host / db_user / db_password / db_database / db_table
- holiday_api / holiday_crawl (둘 중 하나 선택)
