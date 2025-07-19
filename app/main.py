from Parser_Handler import *

def main():
    print("Logs from your program will appear here!\n")
    server_socket: socket.socket = socket.create_server(
        ("localhost", 6379), reuse_port=True                #Creates a server to establish connection between client and cache
    )
    while True:
        try:
            connection: socket.socket                               # Accepts the connection requests from the client
            address: Tuple[str, int]
            connection, address = server_socket.accept()
            client_thread = threading.Thread(                       # Threading used to allow multiple clients to access the cache
                target=Handle_Requests, args=[connection, address]  # Executes the Parser to send responses according to the client requests
            )
            client_thread.start()
        except Exception as e:
            print(f"Exception: {e}")


if __name__ == "__main__":
    main()