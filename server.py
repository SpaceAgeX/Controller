import socket
import subprocess
import os
import webbrowser
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def set_volume(volume_level):
    """Set the system volume to the specified level (0-100)."""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(int(volume_level) / 100, None)

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

def receive_file(conn, file_name, file_size):
    """Receive a file in chunks."""
    received_size = 0
    with open(file_name, 'wb') as f:
        while received_size < file_size:
            file_data = conn.recv(1024)
            if not file_data:
                break
            f.write(file_data)
            received_size += len(file_data)
    print(f"File {file_name} received successfully.")

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

                        if splitUp[0].lower() == "volume":
                            # Change volume
                            volume_level = splitUp[1]
                            set_volume(volume_level)
                            response = f"Volume set to {volume_level}%"
                            conn.sendall(response.encode('utf-8'))
                        
                        elif splitUp[0].lower() == "open":
                            # Open a website
                            url = splitUp[1]
                            webbrowser.open(url)
                            response = f"Website {url} opened."
                            conn.sendall(response.encode('utf-8'))
                        
                        elif splitUp[0].lower() == "update":
                            # Receive and replace the server file
                            file_name = splitUp[1]
                            file_size = int(splitUp[2])
                            print(f"Receiving file: {file_name} with size: {file_size} bytes")
                            receive_file(conn, file_name, file_size)
                            response = f"Server updated with {file_name}."
                            conn.sendall(response.encode('utf-8'))
                            print("Restarting server with new file...")
                            os.execv(file_name, [file_name])  # Restart with new server file
                        
                        elif splitUp[0].lower() == "do":
                            # Execute command
                            command = splitUp[1]
                            os.system(command)
                            response = "done"
                            conn.sendall(response.encode('utf-8'))

                        elif splitUp[0].lower() == "get":
                            # Execute command
                            command = splitUp[1]
                            response = subprocess.check_output(command, shell=True)
                            conn.sendall(response)

                        elif splitUp[0].lower() == "powershell":
                            # Execute PowerShell command
                            powershell_command = None
                            for i in range(1, len(splitUp)):
                                powershell_command += splitUp[i]
                            print(f"PowerShell command: {powershell_command}")    
                            print(f"Executing PowerShell command: {powershell_command}")

                            try:
                                subprocess.call("C:\Windows\System32\powershell.exe + ", shell=True)
                                result = subprocess.check_output(["powershell", "-Command", powershell_command], shell=True)
                                conn.sendall(result)
                            except subprocess.CalledProcessError as e:
                                error_message = f"PowerShell command failed: {e.output.decode('utf-8')}"
                                conn.sendall(error_message.encode('utf-8'))
                    
                    except Exception as e:
                        print(f"Error handling client {addr}: {e}")
                        break  # Break out of the inner loop to listen for new connections
                        
            print("Connection closed. Waiting for new connection...")

if __name__ == "__main__":
    start_server()
