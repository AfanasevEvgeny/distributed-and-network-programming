import sys
from Registry import Registry
from Node import Node
import time
import threading
from xmlrpc.client import ServerProxy
import requests


def main(argv):
    print('Please wait until chord will be filled')
    identifiers_num = 2 ** int(argv[1])
    first_port, last_port = int(argv[2]), int(argv[3])

    nodes_num = last_port - first_port + 1

    registry = Registry(identifiers_num, nodes_num)
    registry.start()

    for node_port in range(nodes_num):
        node = Node(node_port + first_port)
        node.start()

    #     call the methods to get chord info
    #     the time is const, join() is not use
    time.sleep(5)
    chord = ServerProxy('http://localhost:1000')
    print(chord.get_chord_table())


    # .........................Commands to process....................#
    while True:
        print('enter the command:')
        command = input()
        if command.split(' ')[0] == 'get_finger_table':
            node = ServerProxy('http://localhost:' + command.split(' ')[1])
            print(node.get_finger_table())
        if command.split(' ')[0] == 'get_chord_info':
            print(chord.get_chord_table())
        if command.split(' ')[0] == 'save':
            node = ServerProxy('http://localhost:' + command.split(' ')[1])
            print(node.save_file(command.split(' ')[2]))
        if command.split(' ')[0] == 'get':
            node = ServerProxy('http://localhost:' + command.split(' ')[1])
            print(node.get_file(command.split(' ')[2]))
        if command.split(' ')[0] == 'quit':
            try:
                node = ServerProxy('http://localhost:' + command.split(' ')[1])
                print(node.quit_p())
            except ConnectionRefusedError:
                print('The node with port ' + command.split(' ')[1] + ' is not available')




if __name__ == "__main__":
    main(sys.argv[0:])
