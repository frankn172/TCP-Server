# import socket module
from socket import *
import sys  # in order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

# prepare a server socket
serverPort = 1702
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    # establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        # send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n')
        # send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        # send response message for file not file
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n')
        connectionSocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n')
        # close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()  # terminate the program after sending the corresponding data
