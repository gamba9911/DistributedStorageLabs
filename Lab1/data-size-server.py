'''
 Task 5: Send data size

 Extend message type #2 to include the data size before sending the data itself.
 You can choose a number of bytes to encode this information, and make sure the
client never tries to send data more than what can be encoded on this many bytes.
 Alternatively, you can introduce different message types that define the data size bytes.

  For example:
 # String message
 MESSAGE_STRING = 1
 # Data message, data size is encoded on 1 byte (data size: up to 255 bytes)
 MESSAGE_DATA_1B = 2
 # Data message, data size is encoded on 2 bytes (data size: up to 64 kB)
 MESSAGE_DATA_2B = 3
 # Data message, data size is encoded on 3 bytes (data size: up to 16 MB)
 MESSAGE_DATA_3B = 4
 ...

 The server should verify that every byte was received before saving the file.
'''
import socket
import threading
import sys
import random
import string

HOST = 'localhost'
PORT = 9000

# Message types
MESSAGE_STRING = 1
MESSAGE_DATA_1B = 2
MESSAGE_DATA_2B = 3
MESSAGE_DATA_3B = 4


def write_file(data, filename=None):
    if not filename:
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + ".bin"
    with open(filename, 'wb') as f:
        f.write(data)
    print(f"Saved binary data to {filename}")


def recv_exact(conn, size):
    data = b''
    while len(data) < size:
        packet = conn.recv(size - len(data))
        if not packet:
            raise ConnectionError("Connection lost before receiving all data")
        data += packet
    return data


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        message_type = int.from_bytes(conn.recv(1), byteorder=sys.byteorder)

        if message_type == MESSAGE_STRING:
            data = conn.recv(4096)
            print(f"Received string: {data.decode(errors='ignore')}")

        elif message_type in [MESSAGE_DATA_1B, MESSAGE_DATA_2B, MESSAGE_DATA_3B]:
            size_bytes = {MESSAGE_DATA_1B: 1, MESSAGE_DATA_2B: 2, MESSAGE_DATA_3B: 3}[message_type]
            size = int.from_bytes(recv_exact(conn, size_bytes), byteorder=sys.byteorder)
            print(f"Expecting {size} bytes of binary data")
            data = recv_exact(conn, size)
            write_file(data)

        else:
            print("Unknown message type")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
