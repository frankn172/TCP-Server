from socket import *
import sys

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
fileName = sys.argv[3]

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(f'GET /{fileName} HTTP/1.1\r\n'.encode())
clientSocket.send(
    b'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n')
clientSocket.send(f'Host: localhost:{serverPort}\r\n'.encode())
clientSocket.send(b'Connection: close')
clientSocket.send(b'\r\n')
final = ''
message = clientSocket.recv(1024)

while message:
    final += message.decode()
    message = clientSocket.recv(1024)

clientSocket.close()
print(final)
