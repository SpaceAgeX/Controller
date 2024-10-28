import socket

def scan_ip_range(starting_digits, port=65432, timeout=1):
    """
    Scans IP addresses starting with the provided digits, attempting to connect on the specified port.
    If a connection is successful, sends a message to the server and prompts the user to decide whether to continue or stop.
    :param starting_digits: Starting digits of the IP address (e.g., '192.168.')
    :param port: Port to connect to (default is 65432)
    :param timeout: Connection timeout in seconds (default is 1 second)
    """
    # Ensure the starting_digits end with a dot
    if not starting_digits.endswith('.'):
        starting_digits += '.'

    # Iterate over the range of IP addresses (0-255 for each remaining octet)
    for i in range(256):
        for j in range(256):
            ip_address = f"{starting_digits}{i}.{j}"
            print(f"Trying to connect to {ip_address} on port {port}...")

            try:
                # Create a socket object
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(timeout)

                # Attempt to connect to the server
                client_socket.connect((ip_address, port))

                # If connection is successful, send a message to the server
                print(f"Success! Connected to {ip_address}")

                message = "Hello from the IP scanner!"  # Message to send
                client_socket.sendall(message.encode('utf-8'))
                print(f"Sent message to the server: {message}")
                
                # Prompt the user to continue or stop scanning
                user_input = input("Do you want to continue scanning for other IPs? (y/n): ").strip().lower()
                if user_input == 'n':
                    print("Stopping scan as per user request.")
                    client_socket.close()
                    return ip_address  # Return the connected IP

            except (socket.timeout, socket.error):
                # If the connection fails, print the failure and continue scanning
                print(f"Failed to connect to {ip_address}")

            finally:
                client_socket.close()

    # If no connection was made, return None
    print("Finished scanning. No connection found.")
    return None

if __name__ == "__main__":
    # Prompt the user for the starting digits of the IP address
    starting_digits = input("Enter the starting digits of the IP address (e.g., '192.168.'): ")

    # Prompt the user for the timeout (default to 1 second if nothing is entered)
    timeout = input("Enter the connection timeout in seconds (default is 1 second): ")
    timeout = float(timeout) if timeout else 1.0  # Convert input to float or default to 1 second

    # Start scanning for the server
    found_ip = scan_ip_range(starting_digits, timeout=timeout)

    if found_ip:
        print(f"Connected successfully to {found_ip}")
    else:
        print("No server found in the given IP range.")
