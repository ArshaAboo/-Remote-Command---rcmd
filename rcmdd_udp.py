import socket
import sys
import subprocess
from datetime import datetime
import time

def execute_command(command):
    output = subprocess.getoutput(command)
    return output

def main():
    if len(sys.argv) != 2:
        print("Usage: python rcmdd_udp.py <port>")
        sys.exit(1)
    
    host = socket.gethostbyname(socket.gethostname())

    port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    interface_name = "enp7s0" 
    # Get the index of the network interface 
    interface_index = socket.if_nametoindex(interface_name) 
    # Bind host, port and the interface 
    server_socket.bind( ("fe80::30a4:2fff:fe04:40ce", 12345, 0, interface_index) )

    # server_socket.bind((host, port))   

    print(f"UDP Iterative Server is listening on {host,port}...")
    print("""Current Time:{}
hostname: {}
port:{}
Waiting for client.
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), socket.gethostname(), port))
      
    while True:
        message, client_address = server_socket.recvfrom(1024)  

        params = message.decode().split(',')

        if len(params) != 3:
            response = "Invalid message format. Expected: execution_count time_delay command"
        else:
            print("""Incoming client request.
Current Time:{}
Source IP: {}
command:{}

""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), client_address, params[2]))

            execution_count = int(params[0])
            time_delay = float(params[1])

            command = params[2]
            for i in range(execution_count):
                print("Number", i+1, "execution:")
                output = execute_command(command)
                response = 'Execution time: {}, Result: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), output)
                print(response)
                server_socket.sendto(response.encode(), client_address)
                time.sleep(time_delay)
            
            print("""
Current Time:{}
hostname: {}
port:{}
Waiting for client.
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), socket.gethostname(), port))
            
        
if __name__ == "__main__":
    main()
