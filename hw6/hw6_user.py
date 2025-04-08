from socket import *
import time

# 데이터를 저장할 파일 이름
DATA_FILE = "data.txt"

def connect_to_devices():
    """디바이스 1과 디바이스 2에 연결"""
    # 디바이스 1에 연결
    device1_socket = socket(AF_INET, SOCK_STREAM)
    try:
        device1_socket.connect(('localhost', 9001))
        print("디바이스 1에 연결되었습니다.")
    except Exception as e:
        print(f"디바이스 1 연결 실패: {e}")
        device1_socket = None
    
    # 디바이스 2에 연결
    device2_socket = socket(AF_INET, SOCK_STREAM)
    try:
        device2_socket.connect(('localhost', 9002))
        print("디바이스 2에 연결되었습니다.")
    except Exception as e:
        print(f"디바이스 2 연결 실패: {e}")
        device2_socket = None
    
    return device1_socket, device2_socket

def collect_data_from_device1(device1_socket):
    """디바이스 1로부터 데이터 수집"""
    if device1_socket is None:
        print("디바이스 1이 연결되어 있지 않습니다.")
        return None
    
    # 'Request' 메시지 전송
    device1_socket.send("Request".encode())
    
    # 데이터 수신
    data = device1_socket.recv(1024).decode()
    current_time = time.ctime()
    
    # 데이터 포맷팅
    formatted_data = f"{current_time}: Device1: {data}"
    print(formatted_data)
    
    # 데이터 파일에 저장
    with open(DATA_FILE, 'a') as f:
        f.write(formatted_data + '\n')
    
    return formatted_data

def collect_data_from_device2(device2_socket):
    """디바이스 2로부터 데이터 수집"""
    if device2_socket is None:
        print("디바이스 2가 연결되어 있지 않습니다.")
        return None
    
    # 'Request' 메시지 전송
    device2_socket.send("Request".encode())
    
    # 데이터 수신
    data = device2_socket.recv(1024).decode()
    current_time = time.ctime()
    
    # 데이터 포맷팅
    formatted_data = f"{current_time}: Device2: {data}"
    print(formatted_data)
    
    # 데이터 파일에 저장
    with open(DATA_FILE, 'a') as f:
        f.write(formatted_data + '\n')
    
    return formatted_data

def main():
    # 디바이스에 연결
    device1_socket, device2_socket = connect_to_devices()
    
    # 데이터 파일 초기화
    with open(DATA_FILE, 'w') as f:
        f.write("# IoT 디바이스 데이터 수집 결과\n")
    
    try:
        while True:
            # 사용자 입력 받기
            command = input("\n명령어 입력 (1: 디바이스 1 데이터 수집, 2: 디바이스 2 데이터 수집, quit: 종료): ")
            
            if command == '1':
                # 디바이스 1로부터 데이터 수집
                collect_data_from_device1(device1_socket)
                
            elif command == '2':
                # 디바이스 2로부터 데이터 수집
                collect_data_from_device2(device2_socket)
                
            elif command.lower() == 'quit':
                # 종료 명령 전송 및 프로그램 종료
                print("프로그램을 종료합니다.")
                
                # 디바이스 1에 종료 메시지 전송
                if device1_socket:
                    device1_socket.send("quit".encode())
                
                # 디바이스 2에 종료 메시지 전송
                if device2_socket:
                    device2_socket.send("quit".encode())
                
                break
                
            else:
                print("잘못된 명령어입니다. 1, 2, quit 중에서 입력해주세요.")
    
    except Exception as e:
        print(f"오류 발생: {e}")
        
    finally:
        # 소켓 닫기
        if device1_socket:
            device1_socket.close()
        if device2_socket:
            device2_socket.close()
        
        print(f"데이터가 {DATA_FILE} 파일에 저장되었습니다.")

if __name__ == "__main__":
    main()