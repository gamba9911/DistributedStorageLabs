'''
Task 3: Welcome message

 Extend the client to read a string from the standard input, and send that to the server.
 Limit the string size to 4kB (just drop the rest).

 Extend the server to convert the received bytes to string and write it to the console, together
 with the remote IP address. The server should respond by “Message: {received message}“.
'''

from socket import *


def run_server():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('localhost', 9000))  # Local-only server
    s.listen(5)
    print("Server is listening on port 9000...")

    while True:
        c, a = s.accept()
        print(f"Received connection from {a}")
        data = c.recv(4000).decode("utf-8")
        print(f"Message: {data}")
        response = f"Message: {data}"
        c.send(bytes(response, "utf-8"))
        c.close()


if __name__ == "__main__":
    run_server()
