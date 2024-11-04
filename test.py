import socket
import threading
import time

def connect_to_port(host, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a timeout of 5 seconds
        sock.settimeout(5)
        
        # Attempt to connect to the host and port
        sock.connect((host, port))
        
        print(f"Connected to {host}:{port}")
        
        # Close the socket
        sock.close()
        
    except socket.timeout:
        print(f"Connection to {host}:{port} timed out")
        
    except ConnectionRefusedError:
        print(f"Connection to {host}:{port} was refused")
        
    except socket.gaierror:
        print(f"Unable to resolve host {host}")

# Replace 'example.com' with the hostname or IP address you want to connect to
connect_to_port('10.0.30.189', 80)