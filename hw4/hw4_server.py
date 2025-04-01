import socket

def calculate(expression):
    try:
        expression = expression.replace(" ", "")  # 공백 제거
        if '+' in expression:
            num1, num2 = map(int, expression.split('+'))
            return str(num1 + num2)
        elif '-' in expression:
            num1, num2 = map(int, expression.split('-'))
            return str(num1 - num2)
        elif '*' in expression:
            num1, num2 = map(int, expression.split('*'))
            return str(num1 * num2)
        elif '/' in expression:
            num1, num2 = map(int, expression.split('/'))
            return f"{num1 / num2:.1f}"  # 소수점 1자리 표시
        else:
            return "Error: 지원하지 않는 연산"
    except Exception as e:
        return f"Error: {e}"

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 9000))
    s.listen(2)  # 최대 2명의 클라이언트 동시 연결 지원

    while True:
        client, addr = s.accept()
        print('Connection from ', addr)

        while True:
            data = client.recv(1024).decode()
            if not data or data.lower == 'q':  # 클라이언트 종료 요청
                print("종료")
                break
            print('계산식: ', data)
            result = calculate(data)
            client.sendall(result.encode())  # 결과 전송

        client.close()

start_server()