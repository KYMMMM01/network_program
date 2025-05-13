import socket
import select
import sys
import time

# 서버 설정
PORT = 9000
HOST = ''
BUFSIZE = 1024

# 전역 변수 선언
clients = {}  # 클라이언트 정보를 저장할 딕셔너리 (소켓 -> 사용자 이름)

def broadcast(sender_socket, message):
    """
    모든 클라이언트에게 메시지를 전송하는 함수
    """
    global clients  # 전역 변수 clients 사용
    for sock in clients:
        # 메시지를 보낸 클라이언트를 제외한 모든 클라이언트에게 전송
        if sock != sender_socket:
            try:
                sock.send(message.encode())
            except:
                # 전송 실패한 경우 소켓 종료
                sock.close()

def main():
    global clients  # 전역 변수 clients 사용
    
    # 서버 소켓 생성 및 설정
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    
    # select()가 감시할 소켓 리스트
    socket_list = [server_socket]
    
    print("Server Started")
    
    try:
        while True:
            # select() 함수를 사용하여 읽기 가능한 소켓 감시
            readable_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)
            
            # 읽기 가능한 소켓들에 대해 처리
            for sock in readable_sockets:
                # 새로운 클라이언트 연결 요청인 경우
                if sock == server_socket:
                    client_socket, client_addr = server_socket.accept()
                    
                    # 클라이언트 연결 정보 출력
                    print(f"new client {client_addr}")
                    
                    # 클라이언트로부터 사용자 이름 수신
                    username = client_socket.recv(BUFSIZE).decode()
                    
                    # 소켓 리스트에 추가
                    socket_list.append(client_socket)
                    
                    # 클라이언트 정보 딕셔너리에 추가
                    clients[client_socket] = username
                    
                    # 시간 정보와 함께 사용자 이름 출력
                    current_time = time.asctime()
                    print(f"{current_time}{client_addr}:[{username}]")
                    
                    # 접속 메시지 브로드캐스팅
                    # welcome_message = f"[{username}]님이 입장했습니다."
                    # broadcast(client_socket, welcome_message)
                
                # 기존 클라이언트로부터 데이터 수신인 경우
                else:
                    try:
                        # 데이터 수신
                        data = sock.recv(BUFSIZE)
                        
                        # 데이터가 있는 경우
                        if data:
                            message = data.decode()
                            
                            # 'quit' 메시지인 경우 클라이언트 연결 종료 처리
                            if message == 'quit':
                                raise Exception("클라이언트 연결 종료 요청")
                            
                            # 메시지 형식화 및 출력
                            username = clients[sock]
                            client_addr = sock.getpeername()
                            current_time = time.asctime()
                            
                            print(f"{current_time}{client_addr}:[{username}] {message}")
                            
                            # 다른 클라이언트에게 브로드캐스팅
                            formatted_message = f"[{username}] {message}"
                            broadcast(sock, formatted_message)
                        
                        # 데이터가 없는 경우 (연결 종료)
                        else:
                            raise Exception("클라이언트 연결 종료")
                            
                    except Exception as e:
                        # 연결이 종료된 클라이언트 처리
                        # username = clients.get(sock, "알 수 없음")
                        # leave_message = f"[{username}]님이 퇴장했습니다."
                        
                        # 소켓 리스트 및 클라이언트 정보에서 제거
                        if sock in socket_list:
                            socket_list.remove(sock)
                        if sock in clients:
                            del clients[sock]
                        
                        # 소켓 종료
                        sock.close()
                        
                        # 퇴장 메시지 브로드캐스팅
                        # broadcast(sock, leave_message)
            
            # 예외가 발생한 소켓들 처리
            for sock in exception_sockets:
                # 소켓 리스트 및 클라이언트 정보에서 제거
                if sock in socket_list:
                    socket_list.remove(sock)
                if sock in clients:
                    del clients[sock]
                
                # 소켓 종료
                sock.close()
                
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
    finally:
        # 서버 소켓 종료
        server_socket.close()


# 메인 프로그램 실행
if __name__ == "__main__":
    main()