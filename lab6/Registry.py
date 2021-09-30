import threading
from xmlrpc.server import SimpleXMLRPCServer
import random


class Registry(threading.Thread):
    def __init__(self, identifiers_num, nodes_num):
        super().__init__()
        # The number of nodes (m)
        self.nodes_num = nodes_num
        # The number of identifiers (2**m)
        self.identifiers_num = identifiers_num

        # The list of node's dictionaries (id, port)
        self.nodes_list = []

        # List which stores id's info (1: used, 0:not used)
        self.id_list = [0] * identifiers_num

        # Creating registry server
        self.registry_server = SimpleXMLRPCServer(('127.0.0.1', 1000), logRequests=False)
        self.registry_server.register_introspection_functions()
        self.registry_server.register_function(self.register)
        self.registry_server.register_function(self.populate_finger_table)
        self.registry_server.register_function(self.deregister)
        self.registry_server.register_function(self.get_chord_table)

    def run(self):
        print('registry server is listening...')
        self.registry_server.serve_forever()

    # Services

    def register(self, port):
        if self.is_full():
            return -1, 'the Chord is full'
        else:
            generated_id = self.generate_id()
            self.nodes_list.append({'id': generated_id, 'port': port})
            return generated_id, "Success"

    def deregister(self, node_id):
        for i in range(len(self.nodes_list)):
            if self.nodes_list[i] != 0:
                if node_id == self.nodes_list[i]['id']:
                    self.id_list[node_id] = 0
                    self.nodes_list[i] = 0
                    return True
            # ....................new addition for week 7:.............#
        return False

    def populate_finger_table(self, node_id):
        finger_table = [0] * self.nodes_num
        for i in range(1, self.nodes_num + 1):
            finger_table[i - 1] = self.successor(node_id + 2 ** (i - 1))
        predecessor = self.predecessor(node_id)
        return finger_table, predecessor

    # Helper functions

    def generate_id(self):
        random.seed(0)
        is_id_free = True
        node_id = None
        while is_id_free:
            node_id = random.randint(0, self.identifiers_num - 1)
            if self.id_list[node_id] == 0:
                self.id_list[node_id] = 1
                is_id_free = False
        return node_id

    def is_full(self):
        if all(self.id_list):
            return True

    def successor(self, node_id):
        for i in range(node_id + 1, len(self.id_list)):
            if self.id_list[i] != 0:
                return i
        for i in range(0, node_id):
            if self.id_list[i] != 0:
                return i

    def predecessor(self, node_id):
        for i in range(node_id-1, -1, -1):
            if self.id_list[i] != 0:
                return i
        for i in range(node_id + 1, len(self.id_list)):
            if self.id_list[i] != 0:
                return i

    def get_chord_table(self):
        return self.nodes_list
