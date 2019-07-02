# What is this?
It's a simple web server written in python

# Prerequisites
* [Python 3](https://www.python.org/downloads/)

# Importing
import Server class from 
`
server.py
`
```python
from server import Server
```

# Starting the server
* serv = Server( [optional arguments](https://github.com/flametron/python-web-server/wiki/Accepted-arguments) )
* serv.startServer()

# Example
```python
serv = Server(docs="D:\Python-Web-Server-testing\\files",index="abcd.html",logs="D:\Python-Web-Server-testing\logs\logs.txt",customExtensions="html,php")
serv.startServer()
```
