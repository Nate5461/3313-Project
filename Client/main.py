import socket

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
    print("Connected to the server at 127.0.0.1:3000")

    entry = ""
    while entry != "done":
        entry = input("Enter a string to send: ")
        ba = bytearray(entry, 'utf-8')
        written = client_socket.send(ba)

        if written != len(ba):
            print("Wrote: ", written)
            print("The socket appears to have been closed")
            break
        else:
            print("Sent: ", entry)

        data = client_socket.recv(1024)
        if len(data) <= 0:
            print("The socket appears to have been closed")
            break

        print("Received: ", data.decode())

    print("Sleep now")
    client_socket.close()

if __name__ == "__main__":
    main()