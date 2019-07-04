## Examples

* By default the class will use the files under it's own directory with "index.html" as the index file.
* You can specify custom parameters to the server while creating the object by passing the respective parameters from [a list of accepted parameters](https://github.com/flametron/python-web-server/wiki/Accepted-arguments)
* For example, to start a server with html root at D:\ServerFiles\ , you can use the `docs="D:\ServerFiles"` paramter to point the web root to that directory.
* Similarly, you can customize other options of the server as well (with the parameters mentioned [here](https://github.com/flametron/python-web-server/wiki/Accepted-arguments))

### Some given example codes

* ```python
    from server import Server
    serv = Server(docs="D:\ServerFiles",port=445,hostname="mysite.domain")
    serv.startServer()
    ```
    The above code will start a new web server with website root at `D:\ServerFiles`, runing on port `445` with `mysite.domain` as hostname.

* ```python
    from server import Server
    website = Server(customExtensions=["txt"])
    website.startServer()
    ```
    The above code will start the server with `.txt` as a valid file extension to show to the client user agent. The extensions declared by default are: `.php`,`.html`,`.htm`,`.xml`,`.js`,`.css`. Any further extensions passed to Server will be added to this list. If you don't wanna add any custom extensions, put `customExtensions=False` or just omit it altogether.