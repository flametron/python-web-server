import socket

class Server:
    def __init__(self,hostname="localhost",port=80,docs="\\htdocs",index="index.html",connections=5,logs="\\logs\\log.txt"):
        self.port=port
        self.host=hostname
        if not docs.endswith("\\"): docs=docs+"\\"
        self.docroot=docs
        self.maxcons=connections
        self.index=index
        self.logs = logs
        
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
        while True:
            try:
                client_connection, client_address = server_socket.accept()
                request = client_connection.recv(1024).decode("utf-8").split("\n")
                path=request[0].split()[1]
                if not path.endswith("/"):path=path+"/"
                if path=="/": path="{}".format(self.index)
                if path.endswith("/"): path=path+"/{}".format(self.index)
                path=self.docroot+path
                path=path.replace("/","\\").replace("\\\\","\\").replace("\\\\","\\")
                http_response = "HTTP/1.1 200\n\n"+str(open(path,"r").read())
                client_connection.sendall(http_response.encode())
                client_connection.close()
            except FileNotFoundError:
                self.log("Did not find file: {}".format(path))
            except Exception as e:
                self.log("[CRITICAL ERROR]: {}".format(e))
