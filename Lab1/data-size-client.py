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
import sys
import random

HOST = 'localhost'
PORT = 9000

MESSAGE_STRING = 1
MESSAGE_DATA_1B = 2
MESSAGE_DATA_2B = 3
MESSAGE_DATA_3B = 4


def generate_random_bytes(size):
    return bytes(random.getrandbits(8) for _ in range(size))


def send_message(message_type, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(message_type.to_bytes(1, byteorder=sys.byteorder))

        if message_type == MESSAGE_STRING:
            s.send(data)
        elif message_type in [MESSAGE_DATA_1B, MESSAGE_DATA_2B, MESSAGE_DATA_3B]:
            size_bytes = {MESSAGE_DATA_1B: 1, MESSAGE_DATA_2B: 2, MESSAGE_DATA_3B: 3}[message_type]
            size = len(data)
            s.send(size.to_bytes(size_bytes, byteorder=sys.byteorder))
            s.send(data)
        print(f"Sent message of type {message_type} with {len(data)} bytes")


def main():
    while True:
        choice = input("Send (1) string, (2) binary <255B, (3) binary <64KB, (4) binary <16MB, (q) quit: ")
        if choice == 'q':
            break
        elif choice == '1':
            msg = input("Enter message: ")[:4096]
            send_message(MESSAGE_STRING, msg.encode())
        elif choice == '2':
            data = generate_random_bytes(200)
            send_message(MESSAGE_DATA_1B, data)
        elif choice == '3':
            data = generate_random_bytes(5000)
            send_message(MESSAGE_DATA_2B, data)
        elif choice == '4':
            data = generate_random_bytes(1000000)
            send_message(MESSAGE_DATA_3B, data)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
