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


def run_client():
    print("Press Enter to connect to the server. Ctrl+C to exit.")
    while True:
        input()  # Wait for Enter key
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(('localhost', 9000))
            print("Connected to server.")
            s.close()
        except Exception as e:
            print(f"Connection failed: {e}")


if __name__ == "__main__":
    run_client()
