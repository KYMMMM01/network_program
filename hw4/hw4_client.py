import socket

def start_client():    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9000))

    while True:
        expr = input("계산식 입력: ").strip()
        if expr.lower() == 'q':  
            client.sendall(b'q')
            break

        client.send(expr.encode())  # 서버로 수식 전송
        result = client.recv(1024).decode()  # 결과 수신
        print('결과: ', result)

    client.close()

start_client()
 
