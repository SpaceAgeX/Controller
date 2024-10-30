import socket
import threading
import time

# A global flag to indicate when a valid IP address is found
found_ip = None
found_lock = threading.Lock()  # Lock for synchronizing access to the found_ip flag
msg = ""
current_start = 0  # To track the current position in the IP range

def scan_ip(ip_address, port=65432, timeout=5):
    """
    Attempt to connect to the given IP address on the specified port.
    If successful, send a message and receive the server's response.
    If a valid IP is found, set the global flag and stop scanning.
    """
    global found_ip, msg

    # If a valid IP has already been found, exit this thread early
    with found_lock:
        if found_ip is not None:
            return

    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(timeout)

        # Attempt to connect to the server
        client_socket.connect((ip_address, port))

        # If connection is successful, send a message to the server
        print(f"Success! Connected to {ip_address}")

        message = "do:whoami"  # Message to send
        client_socket.sendall(message.encode('utf-8'))
        print(f"Sent message to the server: {message}")

        # Wait for the server's response
        response = client_socket.recv(1024)  # Buffer size of 1024 bytes
        response_decoded = response.decode('utf-8')
        print(f"Received response from server: {response_decoded}")

        # Set the global flag to indicate that we've found a valid IP
        with found_lock:
            if found_ip is None:
                found_ip = ip_address
                # Print the successful IP and response
                msg = f"\n[INFO] Stopping all scans. Found working IP: {found_ip}\n" + f"Response from server: {response_decoded}"
                print(f"\n[INFO] Stopping all scans. Found working IP: {found_ip}")
                #print(f"Response from server: {response_decoded}")
                return

        # Close the connection after the message
        client_socket.close()

    except (socket.timeout, socket.error) as e:
        # If the connection fails, print the failure and continue scanning
        print(f"Failed to connect to {ip_address}: {e}")

    finally:
        client_socket.close()


def scan_ip_range(starting_digits, port=65432, timeout=5, max_threads=256, start_from=0):
    """
    Scans all IP addresses in the range {starting_digits}.0.0 to {starting_digits}.255.255.
    Starts scanning from the given index (start_from).
    Runs multiple threads to parallelize the scanning process.
    Stops when a valid IP address is found.
    """
    global current_start
    threads = []
    current_start = start_from  # Start from this IP index

    for index in range(current_start, 256*256):  # Flattened range from 0 to 65535
        i = index // 256  # First octet (0 to 255)
        j = index % 256  # Second octet (0 to 255)

        

        ip_address = f"{starting_digits}.{i}.{j}"
        print(f"Launching scan for {ip_address}...")

        # Create a thread for each IP address
        thread = threading.Thread(target=scan_ip, args=(ip_address, port, timeout))
        threads.append(thread)
        thread.start()

        # Limit the number of concurrent threads
        if len(threads) >= max_threads:
            for thread in threads:
                thread.join()  # Wait for all threads to finish before launching more
            threads = []  # Reset the thread list after completing a batch

        # Stop launching new threads if a valid IP has been found
        with found_lock:
            if found_ip is not None:
                break

    # Wait for all remaining threads to complete
    for thread in threads:
        thread.join()

    # Update current_start to reflect where we stopped
    current_start = index + 1

    if found_ip is None:
        print("Finished scanning. No valid IP found.")


if __name__ == "__main__":
    # Prompt the user for the first two octets of the IP address
    starting_digits = input("Enter the first two octets of the IP address (e.g., '192.168'): ")

    # Prompt the user for the timeout (default to 5 seconds if nothing is entered)
    timeout = input("Enter the connection timeout in seconds (default is 5 seconds): ")
    timeout = float(timeout) if timeout else 5.0  # Convert input to float or default to 5 seconds

    # Start scanning the IP range from 0
    scan_ip_range(starting_digits, timeout=timeout)

    # After all threads finish, show the message
    
    # Prompt the user if they want to continue scanning
    while True:
        print(msg)
        user_input = input("Do you want to keep scanning for other IPs? (y/n): ").strip().lower()
        if user_input == 'y':
            found_ip = None  # Reset the found_ip to allow a new search
            scan_ip_range(starting_digits, timeout=timeout, start_from=current_start)  # Continue from the last IP
        elif user_input == 'n':
            print("Exiting the program.")
            break
        else:
            print("Please enter 'y' or 'n'.")
