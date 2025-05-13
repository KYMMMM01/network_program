import socket
import threading

# 클라이언트 설정
PORT = 9000
HOST = 'localhost'  # 서버 IP 주소 (로컬 테스트 시 localhost)
BUFSIZE = 1024

def receive_messages(sock):
    """
    서버로부터 메시지를 수신하는 스레드 함수
    """
    while True:
        try:
            # 서버로부터 메시지 수신
            data = sock.recv(BUFSIZE)
            
            # 데이터가 없거나 연결이 끊긴 경우
            if not data:
                print("서버와의 연결이 종료되었습니다.")
                break
                
            # 수신한 메시지 출력 (그대로 출력)
            print(data.decode())
            
        except Exception as e:
            print(f"오류 발생: {e}")
            break

def main():
    # 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 서버에 연결
        client_socket.connect((HOST, PORT))
        
        # 사용자 이름 입력 및 전송
        name = input("ID를 입력하세요: ")
        client_socket.send(name.encode())
        
        # 메시지 수신 스레드 생성 및 시작
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()
        
        # 메시지 입력 및 전송 루프
        while True:
            message = input()
            
            # 'quit' 입력 시 종료
            if message == 'quit':
                client_socket.send('quit'.encode())
                break
                
            # 메시지 전송
            client_socket.send(message.encode())
            
    except Exception as e:
        print(f"연결 오류: {e}")
    finally:
        # 소켓 종료
        client_socket.close()

# 메인 프로그램 실행
if __name__ == "__main__":
    main()