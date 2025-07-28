import socket
import subprocess
import sys
from datetime import datetime
import time
import multiprocessing
import os

# Global flag variable
flag = multiprocessing.Value('b', False)

def handle_session_termination(server_socket, flag):
    while True:
        client_socket_1, addr = server_socket.accept()
        message = client_socket_1.recv(1024).decode()
        if message == "rcend":
            flag.value = True
            print("Session terminated by rcend at client terminal")
            client_socket_1.close()
            break

def handle_client(client_socket, addr, flag):
    # Receive data from the client
    request = client_socket.recv(1024).decode()

    # Parse the request
    execution_count, time_delay, command = request.split(',')
    execution_count = int(execution_count)
    time_delay = float(time_delay)

    print("""Connected to client!
Current Time:{}
Source IP: {}
command:{}
Status: connected

""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), addr, command))

    # Execute the command and send the response
    for i in range(execution_count):
        print("Number", i+1, "execution:")
        output = subprocess.getoutput(command)
        result = 'Execution time: {}, Result: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), output)
        print(result)
        response = f"{len(result):010d}{result}"
        
        client_socket.send(response.encode())
        if (i != execution_count-1):
            time.sleep(time_delay)

    # Close the client connection
    flag.value = True
    client_socket.close()

def main():
    global flag

    if len(sys.argv) != 2:
        print("Usage: python rcmdd_tcp.py <port>")
        sys.exit(1)

    host = socket.gethostbyname(socket.gethostname())
    port = int(sys.argv[1])
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    interface_name = "enp7s0" 
    # Get the index of the network interface 
    interface_index = socket.if_nametoindex(interface_name) 
    # Bind host, port and the interface 
    server_socket.bind( ("fe80::30a4:2fff:fe04:40ce", 12345, 0, interface_index) )

    # Bind the socket to a port
    # server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)

    print(f"TCP server listening on {host,port}")

#     print("""Current Time:{}
# hostname: {}
# port:{}
# Status: closed
# """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), socket.gethostname(), port))
#     print("Waiting for client.") 

    try:
        
        while True:
            print("""
Current Time:{}
hostname: {}
port:{}
Status: closed
Waiting for client.
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), socket.gethostname(), int(sys.argv[1])))

            flag.value =False

            # Accept incoming connections
            client_socket, addr = server_socket.accept()

            # Start the session termination handler process
            termination_process = multiprocessing.Process(target=handle_session_termination, args=(server_socket, flag))
            termination_process.start()

            # Start a new client handling process
            client_process = multiprocessing.Process(target=handle_client, args=(client_socket, addr, flag))
            client_process.start()

            main_pid = os.getpid()

            while True:
            # If flag is set, break out of the loop
                if flag.value:

#                     print("""
# Current Time:{}
# hostname: {}
# port:{}
# Status: closed
# Waiting for client.
#     """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), socket.gethostname(), int(sys.argv[1])))

                    active_processes = multiprocessing.active_children()
                    for p in active_processes:
                        if p.pid != main_pid:
                            p.terminate()

                    break
                    
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        server_socket.close()

if __name__ == "__main__":
    main()
