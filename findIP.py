import socket
import ipaddress

def scan_ip_range(network, port=65432, timeout=1):
    """
    Scans all IP addresses in the provided network, attempting to connect on the specified port.
    :param network: The IP network (e.g., '192.168.1.0/24')
    :param port: Port to connect to (default is 65432)
    :param timeout: Connection timeout in seconds (default is 1 second)
    """
    # Calculate all possible IP addresses in the subnet
    ip_net = ipaddress.ip_network(network, strict=False)
    print(f"Scanning network {ip_net}...")

    # Iterate over all hosts in the subnet
    for ip_address in ip_net.hosts():
        print(f"Trying to connect to {ip_address} on port {port}...")

        try:
            # Create a socket object
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(timeout)

            # Attempt to connect to the server
            client_socket.connect((str(ip_address), port))

            # If connection is successful, send a message to the server
            print(f"Success! Connected to {ip_address}")

            message = "get:whoami"  # Message to send
            client_socket.sendall(message.encode('utf-8'))
            print(f"Sent message to the server: {message}")

            # Wait for the server's response
            response = client_socket.recv(1024)  # Buffer size of 1024 bytes
            print(f"Received response from server: {response.decode('utf-8')}")

            # Close the connection after the message
            client_socket.close()

            # Ask the user if they want to continue scanning
            user_input = input("Do you want to continue scanning for other IPs? (y/n): ").strip().lower()
            if user_input == 'n':
                print("Stopping scan as per user request.")
                return str(ip_address)  # Return the connected IP

        except (socket.timeout, socket.error) as e:
            # If the connection fails, print the failure and continue scanning
            print(f"Failed to connect to {ip_address}: {e}")

        finally:
            client_socket.close()

    # If no connection was made, return None
    print("Finished scanning. No connection found.")
    return None

if __name__ == "__main__":
    # Prompt the user for the network (IP address and subnet mask)
    network = input("Enter the network address with subnet mask (e.g., '192.168.1.0/24'): ")

    # Prompt the user for the timeout (default to 1 second if nothing is entered)
    timeout = input("Enter the connection timeout in seconds (default is 1 second): ")
    timeout = float(timeout) if timeout else 1.0  # Convert input to float or default to 1 second

    # Start scanning for the server
    found_ip = scan_ip_range(network, timeout=timeout)

    if found_ip:
        print(f"Connected successfully to {found_ip}")
    else:
        print("No server found in the given IP range.")
