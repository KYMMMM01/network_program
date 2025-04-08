from socket import *
import random
import time

# 디바이스 1 서버 소켓 생성
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(('localhost', 9001))  # 디바이스 1은 포트 9001 사용
server_socket.listen(1)

print('디바이스 1 서버 시작: 온도, 습도, 조도 측정 (포트 9001)')

# 클라이언트 연결 수락
client_socket, addr = server_socket.accept()
print(f'사용자가 연결되었습니다: {addr}')

try:
    while True:
        # 클라이언트로부터 메시지 수신
        message = client_socket.recv(1024).decode()
        
        # 'quit' 메시지 수신 시 종료
        if message.lower() == 'quit':
            print('종료 메시지를 수신했습니다.')
            break
            
        # 'Request' 메시지 수신 시 데이터 전송
        elif message == 'Request':
            # 임의의 센서 값 생성
            temp = random.randint(0, 40)       # 온도: 0~40
            humid = random.randint(0, 100)     # 습도: 0~100
            illum = random.randint(70, 150)    # 조도: 70~150
            
            # 데이터를 문자열로 변환하여 전송
            data = f"Temp={temp}, Humid={humid}, Illum={illum}"
            client_socket.send(data.encode())
            print(f'데이터를 전송했습니다: {data}')
            
        else:
            print(f'알 수 없는 메시지: {message}')
            
except Exception as e:
    print(f'오류 발생: {e}')
    
finally:
    # 소켓 닫기
    client_socket.close()
    server_socket.close()
    print('디바이스 1 서버를 종료합니다.')