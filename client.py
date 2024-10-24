import socket
import time

def start_client(server_host='127.0.0.1', server_port=65432, timeout=100):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set a timeout for how long we will try to connect before giving up
    client_socket.settimeout(timeout)
    
    print(f"Trying to connect to server at {server_host}:{server_port} (timeout: {timeout} seconds)...")
    
    start_time = time.time()  # Record the current time
    while True:
        try:
            # Try to connect to the server
            client_socket.connect((server_host, server_port))
            print(f"Connected to server at {server_host}:{server_port}")
            break  # Exit the loop if connection is successful
        except (socket.timeout, socket.error) as e:
            # Calculate the time spent trying to connect
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                print(f"Failed to connect to server after {timeout} seconds. Exiting.")
                return  # Exit the client if connection is not successful within timeout

    try:
        # Connection successful, proceed to receive messages
        while True:
            # Wait for a message from the server
            data = client_socket.recv(1024)  # Buffer size of 1024 bytes
            if not data:
                print("Connection closed by the server.")
                break
            
            # Print the message received from the server
            if "shutdown" in data.decode('utf-8'):
                print("Shutting down client...")
            print("Message from server:", data.decode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Always close the socket after usage
        client_socket.close()

if __name__ == "__main__":
    start_client()
