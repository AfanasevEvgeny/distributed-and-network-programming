import socket
import operator

# server configuration

name = 'localhost'
port = 8000
bufferSize = 1024

# create socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# binding socket to port

UDPServerSocket.bind(('localhost', 8001))
print('server is listening')
while True:
    try:
        data, clientAddress = UDPServerSocket.recvfrom(bufferSize)
        expression = data.decode()
        print(type(expression))
        answer = eval(expression)
        print('calculating...')
        UDPServerSocket.sendto(str(answer).encode(), clientAddress)
        print('sent')
    except ZeroDivisionError:
        UDPServerSocket.sendto('Division by zero('.encode(), clientAddress)
    except (SyntaxError, ValueError):
        UDPServerSocket.sendto('Logical error expression'.encode(), clientAddress)
    except NameError:
        UDPServerSocket.sendto('Please, write a math expression with numbers'.encode(), clientAddress)
