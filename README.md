# Remote Command Execution over TCP and UDP (IPv6)

This project implements a client-server system to execute Unix commands remotely using IPv6 over TCP and UDP protocols. The server executes the specified command multiple times with a defined delay and sends both the execution time and command output back to the client. The client displays these results and terminates once all executions are completed.

Features
Supports both TCP and UDP communication.
Implements IPv6 addressing for modern networking compatibility.
Allows remote execution of Unix commands with configurable: Number of executions, Delay between executions
TCP implementation supports session termination using a special command (rcend).
Displays execution time and command output for each run.
Handles multiple client requests indefinitely on the server side.
