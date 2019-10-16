from socket import *
import sys


def main(argv):

    # Check if there exists enough arguments sent
    if (len(argv) >= 2):
        serverName = argv[1]
        serverPort = int(argv[2])
        fileName = argv[3]

    # Set to default if not sent enough arguments
    else:
        serverName = 'localhost'
        serverPort = 1702
        fileName = 'index.html'

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(f'GET /{fileName} HTTP/1.1\n'.encode())
    clientSocket.send(
        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\n'.encode())
    clientSocket.send(f'Host: {serverName}:{serverPort}\n'.encode())
    clientSocket.send('Connection: close\n'.encode())
    clientSocket.send('\r\n'.encode())

    output = 'From Server: '
    message = clientSocket.recv(1024)

    while message:
        output += message.decode()
        message = clientSocket.recv(1024)

    clientSocket.close()
    print(output)


if __name__ == '__main__':
    main(sys.argv)
