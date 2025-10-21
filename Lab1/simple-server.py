"""
 Task 1: Simple server and client

 Implement a socket server in Python, that listens on TCP port 9000 locally for incoming
 connections. When a connection is established, print the remote address to the terminal window
 and close the socket.

 Write a simple client program that connects to the server and print a status message to the
 terminal every time when the user hits the Enter key.
 Both the server and client should run indefinitely until the user terminates the program manually
 (Ctrl+C).

 Notice that the server does not do anything with the received data, and does not send anything
 back.
"""
from socket import *


def run_server():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('localhost', 9000))  # Local-only server
    s.listen(5)
    print("Server is listening on port 9000...")

    while True:
        c, a = s.accept()
        print(f"Received connection from {a}")
        c.close()


if __name__ == "__main__":
    run_server()
