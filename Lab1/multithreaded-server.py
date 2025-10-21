'''
 Task 2: Multithreaded server

 Modify the server code to start a new background thread for each new incoming connection,
 and handle it there.

 Note
 The threading python package overlaps execution of the logical threads in a single physical thread.
 Real parallel execution can be implemented using the multiprocessing package, which starts a new
process and runs a piece of code there.
 However, a new process has a lot higher overhead than a new thread.
 So much that it’s not acceptable when serving small HTTP requests.
'''
import threading
from socket import *


class ConnectionHandler(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        print(f"[Thread Created] Instance address: {hex(id(self))}")

    def run(self):
        print(f"[Handling] Connection from {self.addr} in thread {hex(id(self))}")
        self.conn.close()
#

def run_server():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('localhost', 9000))
    s.listen(5)
    print("Multithreaded server listening on port 9000...")

    while True:
        conn, addr = s.accept()
        handler = ConnectionHandler(conn, addr)
        handler.start()
#

if __name__ == "__main__":
    run_server()
