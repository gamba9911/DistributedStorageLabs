import socket
import threading
import time
import unittest

MSGLEN = 1024  # Define the fixed message length

"""
Demonstration class only- coded for clarity, not efficiency
"""


class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent += sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)


# Simple echo server for testing
def echo_server(host='localhost', port=50007):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            data = conn.recv(MSGLEN)
            conn.sendall(data)


class TestMySocket(unittest.TestCase):
    def setUp(self):
        self.server_thread = threading.Thread(target=echo_server, daemon=True)
        self.server_thread.start()
        time.sleep(1)  # Give the server time to start

    def test_send_receive(self):
        client = MySocket()
        client.connect('localhost', 50007)
        message = b'Hello, world!'.ljust(MSGLEN, b' ')  # Pad message to MSGLEN
        client.mysend(message)
        response = client.myreceive()
        self.assertEqual(response, message)


if __name__ == '__main__':
    unittest.main()
