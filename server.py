import socket
import subprocess

def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
            temp_socket.connect(('8.8.8.8', 80))
            local_ip = temp_socket.getsockname()[0]
        return local_ip
    except Exception as e:
        print(f"Error determining local IP: {e}")
        return '127.0.0.1'

def start_server(port=65432):
    host = get_local_ip()  # Get dynamic local IP
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        print(f"Server started on {host}:{port}")
        
        server_socket.listen(1)
        
        while True:
            print("Waiting for a new connection...")

            # Accept the client connection
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                
                while True:
                    # Receive message from the client
                    data = conn.recv(1024)  # Buffer size of 1024 bytes
                    if not data:
                        # If no data is received, connection is closed by the client
                        print(f"Client {addr} disconnected.")
                        break  # Break the inner loop to accept new connections
                    
                    # Process the message
                    message = data.decode('utf-8')
                    
                    if message.lower() == "shutdown":
                        print("Client requested shutdown. Shutting down server...")
                        return  # Exit the server loop, shutting down the server
                    
                    elif message.lower() == "crash":
                        print("Client requested crash. Crashing server...")
                        return  # Exit the server loop, crashing the server
                    else:
                        try:
                            # Execute the command received from the client
                            response = subprocess.check_output(message, shell=True)
                            # Send the response back to the client (response is already in bytes)
                            conn.sendall(response)
                            print(f"Executed command: {message}, response: {response}")
                        except subprocess.CalledProcessError as e:
                            error_message = f"Command failed: {e}"
                            conn.sendall(error_message.encode('utf-8'))
                            print(error_message)

if __name__ == "__main__":
    start_server()
