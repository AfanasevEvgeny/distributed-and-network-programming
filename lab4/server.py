import socket
import os
import sys
from _thread import *
from random import randrange


def threaded_client(connection):
    num_to_guess = None
    client_range = None
    range_determined = False
    attempts = 5
    connection.send(str.encode('Welcome to the number guessing game!'))
    while True:
        while not range_determined:
            connection.send(str.encode('Enter the range'))
            range_data = connection.recv(2048)
            client_range = range_data.decode()
            try:
                num1, num2 = client_range.split()
                num_to_guess = randrange(int(num1), int(num2))
                print('Client should guess: ', num_to_guess)
                range_determined = True
                connection.send(str.encode('Guess the number:'))
            except ValueError:
                connection.send(str.encode('Error in range '))

        data = connection.recv(2048)
        num = int(data.decode())
        attempts -= 1
        if attempts < 1:
            reply = 'endgame'
        elif num < num_to_guess:
            reply = 'The num is greater'
        elif num > num_to_guess:
            reply = 'The num is less'
        else:
            reply = 'You win!'
            connection.close()
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()


def main(argv):
    server_socket = socket.socket()
    host = '127.0.0.1'
    port = int(argv[0])
    thread_count = 0
    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print('Error while binding to the specified port', str(e))
    print('Server is listening at localhost, port ', port)
    print('Waiting for a Connection..')
    server_socket.listen()
    while True:
        client, address = server_socket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (client,))
        thread_count += 1
        print('Thread Number: ' + str(thread_count))
    server_socket.close()


if __name__ == "__main__":
    main(sys.argv[1:])
