import socket
import os
from os.path import exists

FLAGS = None
class ClientSocket():

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 8000))

    def socket_send(self):
        file_name = input("Input your file name : ")
        if not exists(file_name):
            print("file doesn't exist")
            return

        self.socket.sendto(file_name.encode(), (FLAGS.ip, int(FLAGS.port)))
        total_size = os.path.getsize(file_name)
        self.socket.sendto(str(total_size).encode(), (FLAGS.ip, int(FLAGS.port)))
        
        print("File Transmit Start....")

        start, _ = self.socket.recvfrom(2000)
        isStart = False
        if start.decode() == "start":
            isStart = True

        while isStart:
            file_to_trans = open(file_name, 'rb')
            line = file_to_trans.read(1024)
            current_size = len(line)
            while line:
                self.socket.sendto(line, (FLAGS.ip, int(FLAGS.port)))
                rate = 100 *current_size / total_size
                print("current_size / total_size = "+str(current_size)+"/"+str(total_size)+", "+str(rate)+"%") 
                line = file_to_trans.read(1024)
                current_size += len(line)
            if current_size == total_size:
                try:
                    self.socket.settimeout(5)
                    result, _ = self.socket.recvfrom(2000)
                except socket.timeout:
                    print("timeout error")
                    break
                if result.decode() == 'end':
                    print("ok")
                    break
            file_to_trans.close()
                
        print("file_send_end")
        
    def main(self):
        self.socket_send()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str, default='localhost')
    parser.add_argument('-p', '--port', type=int, default=8080)

    FLAGS, _ = parser.parse_known_args()

    client_socket = ClientSocket()
    client_socket.main()


