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
import threading
import sys
import random
import string

HOST = 'localhost'
PORT = 9000
MAX_STRING_SIZE = 4096
BINARY_SIZE = 8192
MESSAGE_TYPE_STRING = 1
MESSAGE_TYPE_BINARY = 2


def write_file(data, filename=None):
    """
    Write the given data to a local file with the given filename
     :param data: A bytes object that stores the file contents
     :param filename: The file name. If not given, a random string is generated
     :return: The file name of the newly written file, or None if there was an error
    """
    if not filename:
        # Generate random filename
        filename_length = 8
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=filename_length)) + ".bin"
    try:
        # Open filename for writing binary content ('wb')
        with open(filename, 'wb') as f:
            f.write(data)
        print(f"Saved binary data to {filename}")
    except EnvironmentError as e:
        print(f"Error writing file: {e}")
#

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        message_type_bytes = conn.recv(1)
        if not message_type_bytes:
            return
        message_type = int.from_bytes(message_type_bytes, byteorder=sys.byteorder)

        if message_type == MESSAGE_TYPE_STRING:
            data = conn.recv(MAX_STRING_SIZE)
            print(f"Received string from {addr}: {data.decode(errors='ignore')}")
        elif message_type == MESSAGE_TYPE_BINARY:
            data = conn.recv(BINARY_SIZE)
            write_file(data)
        else:
            print(f"Unknown message type from {addr}")
    finally:
        conn.close()
#

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


#

if __name__ == "__main__":
    start_server()
