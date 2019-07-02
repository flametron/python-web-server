import socket
import os

class Server:
    def __init__(self,port=80,docs="\\htdocs",index="index.html",connections=5,logs="\\logs\\log.txt"):
        self.port=port
        if not docs.endswith("\\"): docs=docs+"\\"
        self.docroot=docs
        self.maxcons=connections
        self.index=index
        self.logs = logs
        
    def log(self,entry):
        with open(self.logs,"a") as file:
            file.write("{}: {}\n".format(self.port,entry))
    
    def startServer(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("localhost", self.port))
        server_socket.listen(self.maxcons)
        print("Server listening at {}:{}\nDocument root: {}\nMaximum number of connections: {}".format(socket.gethostname(),self.port,self.docroot,self.maxcons))
        while True:
            try:
                client_connection, client_address = server_socket.accept()
                request = client_connection.recv(1024).decode("utf-8").split("\n")
                path=request[0].split()[1]
                if path=="/": path="/{}".format(self.index)
                path=self.docroot+path
                path=path.replace("/","\\")
                http_response = "HTTP/1.1 200\n\n"+str(open(path,"r").read())
                client_connection.sendall(http_response.encode())
                client_connection.close()
            except FileNotFoundError:
                self.log("Did not find file: {}".format(path))
            except Exception as e:
                self.log("[CRITICAL ERROR}: {}".format(e))

serv = Server(docs="D:\Python-Web-Server\htdocs",logs="D:\Python-Web-Server\logs\logs.txt")
serv.startServer()
