import socket
import os

class Server:
    def __init__(self,hostname="localhost",port=80,docs=os.path.join(os.getcwd(),"htdocs"),index="index.html",connections=5,logs=os.path.join(os.path.join(os.getcwd(),"logs"),"logs.txt"),customExtensions = False, error404=os.path.join(os.path.join(os.getcwd(),"htdocs"),"error404.html")):
        self.error404 = error404
        self.extensions = ["php","js","css","html","xml","htm"]
        self.port=port
        self.host=hostname
        if not docs.endswith("\\"): docs=docs+"\\"
        self.docroot=docs
        self.maxcons=connections
        self.index=index
        self.logs = logs
        self.customExtensions=customExtensions
        if customExtensions:
            for i in customExtensions.split(","):
               if i not in self.extensions:
                   self.extensions.append(i.replace(" ",""))
        
    def log(self,entry):
        try:
            with open(self.logs,"a") as file:
                file.write("{}: {}\n".format(self.port,entry))
        except FileNotFoundError:
            print("Please make sure the path {} exists, error on writing log".format(self.logs))
    
    def startServer(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(self.maxcons)
        print("Server listening at {}:{}\nDocument root: {}\nMaximum number of connections: {}".format(self.host,self.port,self.docroot,self.maxcons))
        print("Index file: {}\n".format(self.index))
        if self.customExtensions:
            print("Custom Valid Extensions: {}".format(self.customExtensions))
        while True:
            try:
                client_connection, client_address = server_socket.accept()
                request = client_connection.recv(1024).decode("utf-8").split("\n")
                path=request[0].split()[1]
                if not path.endswith("/") and path.split(".")[-1] not in self.extensions :path=path+"/"
                if path=="/": path="{}".format(self.index)
                if path.endswith("/"): path=path+"/{}".format(self.index)
                path=self.docroot+path
                path=path.replace("/","\\").replace("\\\\","\\").replace("\\\\","\\")
                http_response = "HTTP/1.1 200\n\n"+str(open(path,"r").read())
                client_connection.sendall(http_response.encode())
                client_connection.close()
            except FileNotFoundError:
                self.log("Did not find file: {}".format(path))
                if self.index in path:
                    http_response = "HTTP/1.1 200\n\n"+str(open(os.path.join(os.path.join(os.getcwd(),"htdocs"),"index.html"),"r").read())
                else:
                    http_response = "HTTP/1.1 404\n\n"+str(open(self.error404,"r").read())                        
                client_connection.sendall(http_response.encode())
                client_connection.close()
            except Exception as e:
                self.log("[CRITICAL ERROR]: {}".format(e))
