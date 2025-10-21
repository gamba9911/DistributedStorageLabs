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
import sys
import os

HOST = 'localhost'
PORT = 9000
CHUNK_SIZE = 4096

MESSAGE_FILENAME = 1
MESSAGE_FILEDATA = 2


def send_files(filenames):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        for filename in filenames:
            if not os.path.exists(filename):
                print(f"File not found: {filename}")
                continue

            with open(filename, 'rb') as f:
                filedata = f.read()

            # Send filename
            s.send(MESSAGE_FILENAME.to_bytes(1, byteorder=sys.byteorder))
            s.send(len(filename.encode()).to_bytes(2, byteorder=sys.byteorder))
            s.send(filename.encode())

            # Wait for OK
            response = s.recv(2)
            if response != b"OK":
                print("Server did not acknowledge filename")
                continue

            # Send file data
            s.send(MESSAGE_FILEDATA.to_bytes(1, byteorder=sys.byteorder))
            s.send(len(filedata).to_bytes(4, byteorder=sys.byteorder))

            sent = 0
            while sent < len(filedata):
                chunk = filedata[sent:sent + CHUNK_SIZE]
                s.send(chunk)
                sent += len(chunk)
            print(f"File {filename} sent successfully")


if __name__ == "__main__":
    # Replace with your actual file names
    send_files(["dummyImage.png", "example2.jpg"])
