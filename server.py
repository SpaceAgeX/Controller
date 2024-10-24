import socket

def start_server(host='127.0.0.1', port=65432):
    # Create a socket object (AF_INET for IPv4, SOCK_STREAM for TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the address and port
        server_socket.bind((host, port))
        print(f"Server started on {host}:{port}")
        
        # Start listening for connections (max 1 connection for simplicity)
        server_socket.listen(1)
        
        # Accept a connection (blocking call until a client connects)
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                # Input from server to send to the client
                message = input("Enter a message to send to the client (type 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("Closing connection.")
                    break
                
                # Send the message to the client
                conn.sendall(message.encode('utf-8'))

if __name__ == "__main__":
    start_server()
