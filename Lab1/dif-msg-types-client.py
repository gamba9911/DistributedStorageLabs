'''
Task 4: Different message types

 Define a message format where you have 2 message types.
 1. Send a short variable length string, up to 4 kB
 2. Send arbitrary size binary data (e.g. file contents).

 The client should first ask the user which type of message they want to send.
 If string type was selected, read the string from the input and send it to the server in a #1 type message.
 If binary type was selected, generate a random byte array and send that to the server as a #2 type message.
 The client should write what happened to the console.
 Keep doing this until the user exits the program
 (e.g. after sending the message, the client should again ask the user what message type to send).
 Close the connection after each message.

 Extend the server to parse the received message, and handle it according to the message type.
 If a string was received, print it to the console.
 If binary data was sent by the client, store it as a file with a random generated filename.
'''
import socket
import sys
import random

HOST = 'localhost'
PORT = 9000
MAX_STRING_SIZE = 4096
BINARY_SIZE = 8192
MESSAGE_TYPE_STRING = 1
MESSAGE_TYPE_BINARY = 2


def generate_random_bytes(size=8192):
    return bytes(random.getrandbits(8) for _ in range(size))


def send_message(message_type, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(message_type.to_bytes(length=1, byteorder=sys.byteorder))
        s.send(data)
        print(f"Sent message of type {message_type}")


def main():
    while True:
        choice = input("Send (1) string or (2) binary? (q to quit): ")
        if choice == 'q':
            break
        elif choice == '1':
            msg = input("Enter message: ")[:MAX_STRING_SIZE]
            send_message(MESSAGE_TYPE_STRING, msg.encode())
        elif choice == '2':
            data = generate_random_bytes(BINARY_SIZE)
            send_message(MESSAGE_TYPE_BINARY, data)
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
