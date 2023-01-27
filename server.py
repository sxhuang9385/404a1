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
        #self.request.sendall(bytearray("OK",'utf-8'))


        #split data to ge the arguments
        string_list = self.data.decode("utf-8").split(" ")
        #get method and path
        method = string_list[0]
        path = string_list[1]

        path = path.lstrip('/')
        path = 'www/' + path
        path += "index.html"

        if method == "GET":
            try:
                file = open(path, "rb")
                content = file.read().encode()
                mimetype = mimetypes.guess_type(path)[0]
                response = "HTTP/1.1 200 OK\nContent-Type: {0}\r\n".format(mimetype) 
            except FileNotFoundError: #needs work
                Error_Msg = "404 Not Found\r\n\n"
                response = "<html><body><center><h3>Error 404: File not found</h3></body></html>\r\n".encode('utf-8')
            except IsADirectoryError: #needs work
                Error_Msg = "301 Moved Permanently\r\n\n"
        #if method isn't "GET"
        else:
            Error_Msg = 'HTTP/1.1 405 Method Not Allowed\r\n'
            final = Error_Msg.encode('utf-8')
            self.request.sendall(final)
            return
        
        #send response
        final = final.encode()
        final = final + response
        self.request.sendall(final)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

