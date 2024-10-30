import socket
import time
import os

def start_client(server_host='127.0.0.1', server_port=65432, retry_delay=5):
    server_host = input("Enter the server's IP address: ")
    
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print(f"Trying to connect to server at {server_host}:{server_port}...")
        try:
            # Attempt to connect to the server
            client_socket.connect((server_host, server_port))
            print(f"Connected to server at {server_host}:{server_port}")
            
            while True:
                try:
                    # Input from user to send to server
                    print("\nMenu:")
                    print("1. Change Volume")
                    print("2. Open Website")
                    print("3. Update Server File")
                    print("4. Send Custom Command")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        volume_level = input("Enter the volume level (0-100): ")
                        message = f"volume:{volume_level}"
                    elif choice == '2':
                        url = input("Enter the website URL: ")
                        message = f"open:{url}"
                    elif choice == '3':
                        # Send server update
                        file_path = input("Enter the path of the new server file: ")
                        if os.path.isfile(file_path):
                            with open(file_path, 'rb') as f:
                                file_data = f.read()
                            message = f"update:{os.path.basename(file_path)}"
                            client_socket.sendall(message.encode('utf-8'))
                            # Send file contents
                            client_socket.sendall(file_data)
                            print("Update sent to the server.")
                            continue
                        else:
                            print("Invalid file path.")
                            continue
                    elif choice == '4':
                        command = input("Enter the custom command: ")
                        message = f"do:{command}"
                    else:
                        print("Invalid choice. Please try again.")
                        continue
                    
                    # Send the message to the server
                    client_socket.sendall(message.encode('utf-8'))
                    
                    # Receive the server's response
                    response = client_socket.recv(1024)
                    print(f"Response from server: {response.decode('utf-8')}")
                
                except Exception as e:
                    print(f"An error occurred while sending or receiving data: {e}")
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
