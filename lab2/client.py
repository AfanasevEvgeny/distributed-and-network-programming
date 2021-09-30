import socket

# Server configuration
serverName = 'localhost'
serverPort = 8001

# creation of socket
clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print('Welcome. Use exit() or Ctrl-Z to exit')
while True:
    try:
        expression = input('Please, write the expression:')
        clientSocket.sendto(expression.encode(), (serverName, serverPort))
        result = clientSocket.recvfrom(1024)[0].decode()
        print('The result is: ', result)
    except KeyboardInterrupt:
        clientSocket.close()
        break
