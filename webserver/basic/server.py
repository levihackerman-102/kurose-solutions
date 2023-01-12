from socket import *
import datetime
import sys


def get_request_line_elements(http_request_str):
    """http_request_str is a str representing a http request.

    Returns a list where each element represents an element of the Request-line.
    0th element - Method
    1st element - Request-URI
    2nd element - HTTP-Version"""

    return http_request_str.split("\n")[0].split(" ")


def create_http_response(status_code_message, body):
    """Creates a HTTP response message using the arguments given. Both of the
    arguments should be strings."""

    response = "HTTP/1.1 " + status_code_message + "\n"
    response += "Date: " + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') + "\n"
    response += "Server: MySimpleServer 0.1\n"
    response += "Content-Type: text/html\n"
    response += "Content-Length: " + str(sys.getsizeof(body)) + "\n"
    response += '\n'
    response += body
    return response


def get_document(uri):
    """Returns a string representing the document found using the uri string given.
    If the file is not found, returns False."""
    try:
        uri = uri.strip("/").replace("/", "\\")
        doc = open(uri, 'r').read()
        return doc
    except IOError:
        return False



serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while 1:
    connectionSocket, addr = serverSocket.accept()
    http_request_str = connectionSocket.recv(2048).decode()

    request_line_elements = get_request_line_elements(http_request_str)

    print("Request-Line elements: ", request_line_elements)

    request_uri = request_line_elements[1]

    print("Request-URI: ", request_uri)

    body = get_document(request_uri)
    
    if body:
        status_code_message = "200 OK"
    else:
        status_code_message = "404 Not Found"
        body = get_document("404.html")

    connectionSocket.send(create_http_response(status_code_message, body).encode())
    connectionSocket.close()
