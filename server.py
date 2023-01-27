#  coding: utf-8 
import socketserver
import mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        #split data to ge the arguments
        string_list = self.data.decode("utf-8").split(" ")

        #get method and path
        method = string_list[0]
        path = string_list[1]

        #if the end of the path is '/' 
        if (path[-1] == '/'):
            path += "index.html"
        path = 'www/' + path

        if method == "GET":
            try:
                file = open(path, "r")
                string = ""
                string = file.read().encode()
                mimetype = mimetypes.guess_type(path)[0]
                response = "HTTP/1.1 200 OK\nContent-Type: " + mimetype + "\r\n" 
            except FileNotFoundError:
                response = "HTTP/1.1 404 Path Not Found\r\n\n"
            except IsADirectoryError:
                response = "HTTP/1.1 301 Moved Permanently\r\n"
        #if method isn't "GET" we can't run it
        else:
            response = 'HTTP/1.1 405 Method Not Allowed\r\n'
            self.request.sendall(response.encode('utf-8'))

        self.request.sendall(response.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
