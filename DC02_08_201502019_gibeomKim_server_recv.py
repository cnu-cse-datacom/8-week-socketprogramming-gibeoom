import socket
FLAGS = None
class ServerSocket():

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 8080))

    def socket_receive(self):
        file_name, addr = self.socket.recvfrom(2000)
        print("file recv start from " + addr[0])
        print(file_name)
        print("File Name :  " + file_name.decode())
        total_size, _ = self.socket.recvfrom(2000)
        total_size = int(total_size.decode())
        print("File Size :  " + str(total_size))

        if total_size > 0:
            self.socket.sendto("start".encode(), (FLAGS.ip, int(FLAGS.port)))
        else :
            return
        
        current_size = 0
        with open('receive', 'wb') as received_file:
            while True:
                try:
                    self.socket.settimeout(5)
                    data, _ = self.socket.recvfrom(1024)
                except socket.timeout:
                    received_file.close()
                    print("timeout error")
                    break

                if not data:
                    break
                current_size += len(data)
                rate = 100 * current_size / total_size
                print("current_size / total_size = "+str(current_size)+"/"+str(total_size)+", "+str(rate)+"%")
                received_file.write(data)
                if current_size == total_size:
                    self.socket.sendto("end".encode(), (FLAGS.ip, int(FLAGS.port)))
                    received_file.close()
                    break
            
    def main(self):
        self.socket_receive()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str, default='localhost')
    parser.add_argument('-p', '--port', type=int, default=8000)

    FLAGS, _ = parser.parse_known_args()

    server_socket = ServerSocket()
    server_socket.main()


