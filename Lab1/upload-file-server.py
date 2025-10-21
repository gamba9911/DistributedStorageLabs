"""
 Task 6: Upload a file

 Copy a few test files to the directory where the client is.

 The client reads a filename string (e.g. “test.pdf”) from the user in each iteration of the main while loop.
 When it’s given, the client tries to read the file from its local folder into the memory.
 If the file exists, the client first sends the file name to the server as a #1 type message, and waits for a response.
 If the response is the string “OK”, the client sends the file contents as a #2 type message (including data size)
  and close the connection.

 The server writes the file contents to the local folder, using the given file name.

 Both the client and server must handle files over 4kB correctly (send and receive multiple chunks).

 Extra task 1 : After a file upload is complete, keep the socket connection open and re-use the
 same socket for additional uploads.

 Extra task 2 : Create the file on the server immediately when you receive the file name, and
 append to the contents every time you receive data. This way you are not allocating memory for
 the whole file on the server until all fragments arrive.
"""
import socket
import threading
import sys

HOST = 'localhost'
PORT = 9000
CHUNK_SIZE = 4096

MESSAGE_FILENAME = 1
MESSAGE_FILEDATA = 2


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
        while True:
            message_type_bytes = conn.recv(1)
            if not message_type_bytes:
                break
            message_type = int.from_bytes(message_type_bytes, byteorder=sys.byteorder)

            if message_type == MESSAGE_FILENAME:
                filename_length = int.from_bytes(recv_exact(conn, 2), byteorder=sys.byteorder)
                filename = recv_exact(conn, filename_length).decode()
                filename = "copy_" + filename
                print(f"Receiving file: {filename}")
                conn.sendall(b"OK")
                f = open(filename, 'wb')  # Open file immediately

            elif message_type == MESSAGE_FILEDATA:
                filesize = int.from_bytes(recv_exact(conn, 4), byteorder=sys.byteorder)
                print(f"Expecting {filesize} bytes")
                received = 0
                while received < filesize:
                    chunk = conn.recv(min(CHUNK_SIZE, filesize - received))
                    if not chunk:
                        raise ConnectionError("Connection lost during file transfer")
                    f.write(chunk)
                    received += len(chunk)
                f.close()
                print(f"File {filename} saved successfully")

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
