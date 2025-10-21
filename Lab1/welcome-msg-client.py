'''
Task 3: Welcome message

 Extend the client to read a string from the standard input, and send that to the server.
 Limit the string size to 4kB (just drop the rest).

 Extend the server to convert the received bytes to string and write it to the console, together
 with the remote IP address. The server should respond by “Message: {received message}“.
'''

from socket import *


def run_client():
    print("Type your message and press Enter to send. Ctrl+C to exit.")
    while True:
        data = input("Message: ")
        try:
            with socket(AF_INET, SOCK_STREAM) as s:
                s.connect(('localhost', 9000))
                s.send(bytes(data[:4000], "utf-8"))
                response = s.recv(4096).decode("utf-8")
                print(f"Server response: {response}")
        except Exception as e:
            print(f"Connection failed: {e}")


if __name__ == "__main__":
    run_client()
