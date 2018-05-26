# -*- coding: utf-8 -*-
import select
import socket
import struct
from datetime import datetime

#_HOST = '127.0.0.1'
_PORT = 20000

class Visualize:
    MAX_WAITING_CONNECTIONS = 100
    RECV_BUFFER = 4096
    RECV_msg_content = 4
    RECV_MSG_TYPE_LEN = 4

    def __init__(self, port):
        # store the data
        self.data_dic = {}

        self.port = port
        self.connections = [] # collects all the incoming connections
        self.load_config()
        self.log_init()
        self._run()

    def log_init(self):
        try:
            self.log_file = open("./log/publisher.log", "w+")
            self.log_file.close()
        except Exception, e:
            print(Exception, ", ", e)

    def load_config(self):
        try:
            with open('./config/publisher.conf') as f:
                for line in f:
                    if line[0] != '#':
                        line = line.split()
                        self.data_dic[line[0]] = line[1]

        except Exception, e:
            print(Exception, ", ", e)
            raise SystemExit

    def _bind_socket(self):
        """
        Create the sever socket and bind it to the given host and port
        :return:
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('', self.port))
        self.server_socket.listen(self.MAX_WAITING_CONNECTIONS)
        self.connections.append(self.server_socket)

    def _receive(self, sock):
        """
        first get length
        then get type
        process
        :return:
        """
        try:
            message = sock.recv(2048)
            print(message)
        except Exception, e:
            print(Exception, ", ", e)

        print("\n**********************************************\n")

    def _run(self):
        self._bind_socket()
        while True:
            """
            Actually runs the server.
            """
            # Gets the list of sockets which are ready to be read through select non-blocking calls
            # The select has a timeout of 60 seconds
            try:
                ready_to_read, ready_to_write, in_error = select.select(self.connections, [], [], 60)
            except socket.error:
                continue
            else:
                for sock in ready_to_read:
                    if sock == self.server_socket:
                        if sock == self.server_socket:
                            try:
                                # Handles a new client connection
                                client_socket, client_address = self.server_socket.accept()
                            except socket.error:
                                break
                            else:
                                self.connections.append(client_socket)
                                print "Client (%s, %s) connected" % client_address
                        # ... else is an incoming client socket connection
                    else:
                        try:
                            #next_route_ip, data = self._receive(sock)
                            self._receive(sock)
                        except socket.error:
                            #print("Client is offline" % client_address)
                            sock.close()
                            self.connections.remove(sock)
                            continue


p = Visualize(_PORT)