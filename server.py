import socket

def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        # Create a temporary socket to connect to an external server to get the local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
            # We don't actually connect to Google's DNS server, we just use it to get the local IP
            temp_socket.connect(('8.8.8.8', 80))
            local_ip = temp_socket.getsockname()[0]  # Get the local IP from the temp socket
        return local_ip
    except Exception as e:
        print(f"Error determining local IP: {e}")
        return '127.0.0.1'  # Fallback to localhost if unable to determine

def start_server(port=65432):
    # Dynamically determine the local IP address
    host = get_local_ip()
    
    # Create a socket object (AF_INET for IPv4, SOCK_STREAM for TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the dynamically determined address and port
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
