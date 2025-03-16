import os
import signal
import socket
import subprocess
import sys
import time  # For adding delay
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

# Function to check if the port is in use and get the PID
def check_and_kill_port(port):
    try:
        # Check if the port is in use by trying to bind to it
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", port))
            return False  # Port is available
    except OSError as e:
        if e.errno == 98:  # Port is already in use
            print(f"Port {port} is already in use, checking PID...")
            try:
                # Find the PID using `lsof` (for Unix-like OS)
                pid = subprocess.check_output(["lsof", "-t", "-i", f":{port}"]).strip()
                
                if pid:
                    pid = int(pid)
                    print(f"Killing process with PID: {pid}")
                    os.kill(pid, signal.SIGKILL)
                    return True  # Port was used, and we killed the process
                else:
                    print(f"No process found using port {port}.")
                    return False
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while trying to get the PID for port {port}: {e}")
                return False  # Error occurred, we don't kill anything
            except PermissionError:
                print("Permission denied: you may need to run the script with elevated privileges.")
                return False
            except Exception as e:
                print(f"Unexpected error while killing process: {e}")
                return False


# Function to start the server
def start_server(port):
    # Serve the index.html template using the built-in HTTP server
    print(f"Starting server on port {port}...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Make sure the server runs in the script's directory
    handler = SimpleHTTPRequestHandler
    httpd = TCPServer(("", port), handler)
    httpd.serve_forever()


def main():
    port = 8000  # Port to use for the server

    # Check and kill the process if the port is in use
    if check_and_kill_port(port):
        print(f"Waiting for the port {port} to be released...")
        time.sleep(2)  # Give some time for the port to be released
        
        print(f"Restarting the server on port {port}...")
        # Restart the script itself after killing the process
        subprocess.Popen([sys.executable] + sys.argv)  # Run the script again
        sys.exit()  # Exit the current instance of the script

    # Start the server
    start_server(port)


if __name__ == "__main__":
    main()

