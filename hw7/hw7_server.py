import socket
from collections import defaultdict

port = 2500
BUFFSIZE = 1024

# 메시지 박스 초기화 (defaultdict 사용)
message_boxes = defaultdict(list)

# UDP 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', port))
print(f"UDP 서버가 포트 {port}에서 시작되었습니다...")

while True:
    msg, addr = sock.recvfrom(BUFFSIZE)
    msg_decoded = msg.decode()
    print('Received: ', msg_decoded)
    
    # 'quit' 명령 처리
    if msg_decoded.strip() == "quit":
        print("서버를 종료합니다...")
        break
    
    # 메시지 파싱
    parts = msg_decoded.split(' ', 2)
    command = parts[0].lower()
    
    # 'send' 명령 처리
    if command == "send" and len(parts) >= 3:
        mbox_id = parts[1]
        content = parts[2]
        message_boxes[mbox_id].append(content)
        sock.sendto("OK".encode(), addr)
    
    # 'receive' 명령 처리
    elif command == "receive" and len(parts) == 2:
        mbox_id = parts[1]
        if mbox_id not in message_boxes or not message_boxes[mbox_id]:
            sock.sendto("No messages".encode(), addr)
        else:
            # 첫 번째 메시지 반환 및 삭제
            message = message_boxes[mbox_id].pop(0)
            sock.sendto(message.encode(), addr)
    
    # 잘못된 명령 처리
    else:
        sock.sendto("Invalid command".encode(), addr)

# 소켓 종료
sock.close()