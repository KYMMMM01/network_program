from socket import *
import os

# 웹 서버 소켓 생성
s = socket()
s.bind(('', 80))  # 포트 번호 80으로 바인딩
s.listen(10)  # 최대 10개의 연결 대기

print('웹 서버가 시작되었습니다. 포트 번호: 80')

while True:
    # 클라이언트 연결 수락
    c, addr = s.accept()
    print(f'클라이언트가 연결되었습니다: {addr}')
    
    # 클라이언트로부터 HTTP Request 수신
    data = c.recv(1024)
    msg = data.decode()
    
    # HTTP 요청 메시지 파싱
    req = msg.split('\r\n')
    
    # 요청 라인 파싱 (예: GET /index.html HTTP/1.1)
    req_line = req[0].split()
    
    # 요청된 파일 경로 추출 (예: /index.html -> index.html)
    if len(req_line) > 1:
        path = req_line[1]
        filename = path[1:] if path.startswith('/') else path
    else:
        filename = ""
    
    print(f'요청된 파일: {filename}')
    
    # 기본 파일이 요청되지 않은 경우 index.html로 설정
    if filename == "":
        filename = "index.html"
    
    try:
        # 파일 타입에 따른 처리
        if filename.endswith('.html'):
            # HTML 파일 처리
            f = open(filename, 'r', encoding='utf-8')
            mimeType = 'text/html'
            data = f.read()
            f.close()
            
            # HTTP 응답 헤더 생성
            header = 'HTTP/1.1 200 OK\r\n'
            header += f'Content-Type: {mimeType}\r\n'
            header += '\r\n'
            
            # HTTP 응답 전송 (헤더 + 바디)
            c.send(header.encode('utf-8'))
            c.send(data.encode('euc-kr'))  # HTML은 euc-kr로 인코딩하여 전송
            
        elif filename.endswith('.png'):
            # PNG 이미지 파일 처리
            f = open(filename, 'rb')
            mimeType = 'image/png'
            data = f.read()
            f.close()
            
            # HTTP 응답 헤더 생성
            header = 'HTTP/1.1 200 OK\r\n'
            header += f'Content-Type: {mimeType}\r\n'
            header += '\r\n'
            
            # HTTP 응답 전송 (헤더 + 바디)
            c.send(header.encode('utf-8'))
            c.send(data)  # 바이너리 데이터는 그대로 전송
            
        elif filename.endswith('.ico'):
            # ICO 파일 처리
            f = open(filename, 'rb')
            mimeType = 'image/x-icon'
            data = f.read()
            f.close()
            
            # HTTP 응답 헤더 생성
            header = 'HTTP/1.1 200 OK\r\n'
            header += f'Content-Type: {mimeType}\r\n'
            header += '\r\n'
            
            # HTTP 응답 전송 (헤더 + 바디)
            c.send(header.encode('utf-8'))
            c.send(data)  # 바이너리 데이터는 그대로 전송
            
        else:
            # 지원하지 않는 파일 또는 파일이 존재하지 않는 경우
            raise FileNotFoundError
            
    except FileNotFoundError:
        # 404 Not Found 응답 생성
        header = 'HTTP/1.1 404 Not Found\r\n'
        header += '\r\n'
        body = '<html><head><title>Not Found</title></head><body>Not Found</body></html>'
        
        # HTTP 응답 전송 (헤더 + 바디)
        c.send(header.encode('utf-8'))
        c.send(body.encode('utf-8'))
    
    # 연결 종료
    c.close()