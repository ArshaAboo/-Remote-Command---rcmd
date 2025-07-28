import socket
import sys
import threading

flag = False

def client_input_listener(server_ip, server_port):
    global flag
    while True:
        client_socket_1 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        client_socket_1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        interface_name = "enp7s0" 
    # Get the index of the network interface 
        interface_index = socket.if_nametoindex(interface_name) 
    # Bind host, port and the interface 
        client_socket_1.bind( ("fe80::30b5:e4ff:fe7a:2359", 5000, 0, interface_index) )
        
        
        client_socket_1.connect((server_ip, server_port))

        message = input("")
        if message == "rcend":
            client_socket_1.send(message.encode())
            print("Terminating session...")
            flag = True
            client_socket_1.close()

            break


def receive_response(client_socket,execution_count):
    global flag
    try:
        # Receive and print the responses from the server
        for i in range(execution_count):
        
            response_length = int(client_socket.recv(10).decode()) 
            response = client_socket.recv(response_length).decode()
            print("Number", i+1, "execution:")
            print(response)

        # Close the connection
        print("All work has been done. Terminating session.")
        flag = True
    except ConnectionResetError:
        print("Connection reset by peer. Server may have closed the connection unexpectedly.")

    # client_socket.close()



def main():
    global flag
    # Parse command-line arguments
    server_hostname = sys.argv[1]
    server_port = int(sys.argv[2])
    execution_count = int(sys.argv[3])
    time_delay = float(sys.argv[4])
    command = sys.argv[5]

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # server_ip = socket.gethostbyname(server_hostname)
    server_ip = socket.getaddrinfo(server_hostname, None, socket.AF_INET6)[0][4][0]
    
    interface_name = "enp7s0" 
    # Get the index of the network interface 
    interface_index = socket.if_nametoindex(interface_name) 
    # Bind host, port and the interface 
    client_socket.bind( ("fe80::30b5:e4ff:fe7a:2359", 12345, 0, interface_index) )

    # Connect to the server
    client_socket.connect((server_ip, server_port))

      # Send the command to the server
    request = f"{execution_count},{time_delay},{command}"
    client_socket.send(request.encode())

    #daemon threads will automatically exit when the main thread exits.
    threading.Thread(target=client_input_listener,args =(server_ip,server_port),daemon=True).start()
    threading.Thread(target=receive_response,args =(client_socket,execution_count),daemon=True).start()

    while True:
        if flag:
            break

    client_socket.close()
    
if __name__ == "__main__":
    main()



# The program has 2 threads which are DAEMON threads. ONE THREAD FOR HANDLING RCEND INPUT FROM USER.
# OTHER THREAD TO HANDLE RECEIVING FROM SERVER.
# GLOBAL VARIABLE FLAG SET TO TRUE AT THE END OF EACH OF THESE THREADS.
# AFTER THREAD.START(), MAIN PROGRAM CHECKS FOR FLAG == TRUE IN A WHILE LOOP, WHICH WILL BE USED AS A CONDITION CHECK TO EXIT THE MAIN PROGRAM.
# SINCE THE TWO THREADS ARE DAEMON, WHEN MAIN PROGRAM EXITS, WHICHEVER THREAD IS STILL ACTIVE WILL BE TERMINATED TOO.



