import socket
import sys

def main():
    if len(sys.argv) != 6:
        print("Usage: python rcmd_udp.py <server_hostname> <port> <execution_count> <time_delay> <command>")
        sys.exit(1)
    
    server_hostname = sys.argv[1]
    port = int(sys.argv[2])
    execution_count = int(sys.argv[3])
    time_delay = float(sys.argv[4])
    command = sys.argv[5]

    # server_ip = socket.gethostbyname(server_hostname)
    server_ip = socket.getaddrinfo(server_hostname, None, socket.AF_INET6)[0][4][0]
    
    client_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    
    interface_name = "enp7s0" 
# Get the index of the network interface 
    interface_index = socket.if_nametoindex(interface_name) 
# Bind host, port and the interface 
    client_socket.bind( ("fe80::30d4:a5ff:fed6:b6b5", 12345, 0, interface_index) )
    
    
    client_socket.sendto(f"{execution_count},{time_delay},{command}".encode(), (server_ip, port))

    for i in range(int(execution_count)):
            data, server_address = client_socket.recvfrom(1024)
            response = data.decode('utf-8')
            print("Number", i+1, "execution:")
            print(response)
    
    print("All work has been done")

if __name__ == "__main__":
    main()