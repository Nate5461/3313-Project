import socket
import sys
import select

def create_client_socket():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = ('127.0.0.1', 3000)

    # Connect the socket to the server
    client_socket.connect(server_address)

    return client_socket

def main():
    client_socket = create_client_socket()
    client_socket.setblocking(0)
    print("Connected to the server at 127.0.0.1:3000")

    while True:
        ready_to_read, _, _ = select.select([client_socket, sys.stdin], [], [])
        for s in ready_to_read:
            if s == client_socket:
                data = client_socket.recv(1024)
                if len(data) <= 0:
                    print("The socket appears to have been closed")
                    return
                print("Received: ", data.decode())
            else:
                entry = input()
                if entry == "done":
                    print("Sleep now")
                    client_socket.close()
                    return
                ba = bytearray(entry, 'utf-8')
                written = client_socket.send(ba)
                if written != len(ba):
                    print("Wrote: ", written)
                    print("The socket appears to have been closed")
                    return
                else:
                    print("Sent: ", entry)

if __name__ == "__main__":
    main()