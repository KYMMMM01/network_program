import socket
import struct
import binascii

class Udphdr:
    def __init__(self, src_port, dst_port, length, checksum):
        self.src_port = src_port    # 송신자 포트번호 (2바이트)
        self.dst_port = dst_port    # 수신자 포트번호 (2바이트)
        self.length = length        # UDP 패킷 길이 (2바이트)
        self.checksum = checksum    # 체크섬 (2바이트)
    
    def pack_Udphdr(self):
        packed = b''
        packed += struct.pack('!HHHH', self.src_port, self.dst_port, 
                             self.length, self.checksum)
        return packed

def unpack_Udphdr(buffer):
    unpacked = struct.unpack('!HHHH', buffer[:8])
    return unpacked

def getSrcPort(unpacked_udpheader):
    return unpacked_udpheader[0]

def getDstPort(unpacked_udpheader):
    return unpacked_udpheader[1]

def getLength(unpacked_udpheader):
    return unpacked_udpheader[2]

def getChecksum(unpacked_udpheader):
    return unpacked_udpheader[3]

# UDP 헤더 생성 및 테스트
udp = Udphdr(5555, 80, 1000, 0xFFFF)
packed_udphdr = udp.pack_Udphdr()
print(binascii.b2a_hex(packed_udphdr))

# UDP 헤더 언팩 및 필드 값 확인
unpacked_udphdr = unpack_Udphdr(packed_udphdr)
print(unpacked_udphdr)
print("Source Port: {}".format(getSrcPort(unpacked_udphdr)))
print("Destination Port: {}".format(getDstPort(unpacked_udphdr)))
print("Length: {}".format(getLength(unpacked_udphdr)))
print("Checksum: 0x{:04X}".format(getChecksum(unpacked_udphdr)))