import socket
from typing import Tuple
import threading

values = {}

def Handle_Requests(conn: socket.socket, addr: Tuple[str, int]) -> None:
    with conn:
        print(f"Accepted connection from {addr}\n")
        while True:
            try:
                recv_data = conn.recv(1024)         #receives data from the client
                if not recv_data:
                    break
                if "" == recv_data.decode():
                    continue
                data = [
                    element
                    for element in recv_data.decode().split("\r\n")  #Splits the received message into RESP format
                    if element.strip()
                ]

                if not data or len(data) < 3:
                    break

                command = data[2].lower()

                match command:                                      #Sends response to the client based on their requests 
                    case "ping":
                        response = "+PONG\r\n"
                    case "echo":
                        if len(data) >= 5:
                            response = f"+{data[4]}\r\n"
                    case "set":
                        if len(data) >= 7:
                            values[data[4]] = data[6]
                            response = "+OK\r\n"
                        if len(data) >= 9:
                            match data[8].lower():
                                case "px":
                                    time = int(data[10])
                                    threading.Timer(
                                        time / 1000, values.pop, args=[data[4]]
                                    ).start()
                    case "get":
                        if len(data) >= 5:
                            key = data[4]
                            if key not in values:
                                response = "$-1\r\n"
                            else:
                                response = f"${len(values.get(key))}\r\n{values.get(key)}\r\n"
                    case _:
                        response = f"-ERR Unknown command\r\n"
                conn.sendall(response.encode())
            except Exception as e:
                print(f"Error while handling client: {e}")          # Error Handling for unexpected arguments from the client
                conn.sendall(b"-ERR Internal server error\r\n")
                break

