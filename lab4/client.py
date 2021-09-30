import socket
import sys


def main(argv):
    client_socket = socket.socket()
    try:
        host = argv[0]
        port = int(argv[1])
    except IndexError:
        print(' Usage example: python./client.py <address> <port>')
        exit()
    can_answer = True

    print('Waiting for connection')
    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print(str(e))

    response = client_socket.recv(1024)
    print(response.decode())
    range_validated = False
    while not range_validated:
        Input = input('Enter the range')
        client_socket.send(Input.encode())
        response = client_socket.recv(1024).decode()
        print(response)
        if response == 'Guess the number:':
            range_validated = True

    while can_answer:
        Input = input()
        client_socket.send(str.encode(Input))
        response = client_socket.recv(1024)
        print(response.decode())
        if response.decode() == 'endgame':
            print('You lose')
            can_answer = False
        elif response.decode() == 'You win!':
            can_answer = False

    client_socket.close()


if __name__ == "__main__":
    main(sys.argv[1:])
