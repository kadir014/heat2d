import socket
import threading
import time
from heat2d.errors import NetworkingError

HOSTNAME  = socket.gethostname()
LOCALHOST = socket.gethostbyname(HOSTNAME)


class Header:

    def __init__(self, string):
        i = 1
        s = ""
        self.fields = list()

        while i < len(string)+1:
            if string[i] == "}": break
            if string[i] == "/":
                self.fields.append(s)
                continue
            s += string[i]

    def __repr__(self):
        return f"<heat2d.networking.Header({self.fields})>"


class ConnectedClient(threading.Thread):

    def __init__(self, s, address, id, server):
        super().__init__()
        self.socket = s
        self.address = address[0]
        self.port = address[1]
        self.id = id
        self.server = server
        self.__is_alive  = True

        self.package = ""
        self.header = None

    def __repr__(self):
        return f"<heat2d.networking.ConnectedClient(id={self.id}, {self.address}:{self.port})>"

    def run(self):
        print(f"New client has connected {self}")

        while self.__is_alive :
            s = self.socket.recv(1024).decode("utf-8")

            if not self.header:
                self.header = Header(s[:s.find("}")])
                self.package += s[9:]

            else:
                if len(self.package) > int(self.header.fields[0]):
                    self.package = ""
                    self.header = None
                    if self.header.fields[1] == "str":
                        self.server.callback("string_received", str, self)
                        self.socket.send("{0/ping}".encode("utf-8"))
                    continue
                self.package += s

            #if len(str) > 0:
            #    self.server.callback("message_received", str, self)
            #    self.socket.send(f"Message '{str}' received succesfully.".encode("utf-8"))


class Server(threading.Thread):

    def __init__(self, address, port):
        super().__init__()
        self.address, self.port = address, port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = list()
        self.event_funcs = dict()
        self.__is_alive = True

    def __repr__(self):
        return f"<heat2d.networking.Server({self.address}:{self.port})>"

    def event(self, func):
        self.event_funcs[func.__name__] = func

    def callback(self, eventname, *args, **kwargs):
        if eventname in self.event_funcs: self.event_funcs[eventname](*args, **kwargs)

    def run(self):
        self.socket.bind((self.address, self.port))
        self.socket.listen(5)

        print(f"Server started listening on {self.address}:{self.port}\n")

        while self.__is_alive:
            connection = self.socket.accept()
            connectedclient = ConnectedClient(connection[0], connection[1], len(self.clients), self)
            connectedclient.start()
            self.clients.append(connectedclient)


class Connection(threading.Thread):

    def __init__(self, address, port):
        super().__init__()
        self.address, self.port = address, port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event_funcs = dict()
        self.latency = 0
        self.l_start = 0
        self.__is_alive  = True

    def __repr__(self):
        return f"<heat2d.networking.Connection({self.address}:{self.port})>"

    def event(self, func):
        self.event_funcs[func.__name__] = func

    def callback(self, eventname, *args, **kwargs):
        if eventname in self.event_funcs: self.event_funcs[eventname](*args, **kwargs)

    def send_str(self, s):
        self.l_start = time.time()
        self.socket.send(f"{{{len(s)}/str}}{s}".encode("utf-8"))

    def run(self):
        self.socket.connect((self.address, self.port))
        print(f"Connection established with {self.address}:{self.port}")

        while self.__is_alive :
            s = self.socket.recv(1024).decode("utf-8")

            if not self.header:
                self.header = Header(s[:s.find("}")])
                self.package += s[9:]

            else:
                if len(self.package) > int(self.header.fields[0]):
                    self.package = ""
                    self.header = None
                    if self.header.fields[1] == "ping": self.latency = time.time() - self.start_l
                    continue
                self.package += s

        # send server : client disconnected
        self.socket.close()


def initialize_server(address, port=1234):
    if not address: raise NetworkingError("No address has been passed.")
    return Server(address, port)

def create_connection(address, port=1234):
    if not address: raise NetworkingError("No address has been passed.")
    conn = Connection(address, port)
    conn.start()
    return conn
