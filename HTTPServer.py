# import socket module
from socket import *
import sys  # in order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

# prepare a server socket
serverPort = 1702

# tell kernel to reuse local socket without waiting for its natural timeout to expire
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:

    # establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()
        print(message)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\n'.encode())
        connectionSocket.send('Connection: close\n'.encode())
        connectionSocket.send(
            'Content-Length: {}\n'.format(len(outputdata)).encode())
        connectionSocket.send('Content-Type: text/html\n'.encode())
        connectionSocket.send('\n'.encode())

        # send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError as err:

        print("ERROR: ")
        print(err)
        print()

        # send response message for file not file
        connectionSocket.send('HTTP/1.1 404 Not Found\n'.encode())
        connectionSocket.send('Connection: close\n'.encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.send(
            '<html><head></head><body><h1>404 Not Found</h1></body></html>\n'.encode())
        connectionSocket.send('\r\n'.encode())

        # close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()  # terminate the program after sending the corresponding data
