import threading
import time
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
import random


class Node(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.proxy = None
        self.port = int(port)
        self.id = None
        self.is_quited = False
        self.finger_table = []
        self.server = SimpleXMLRPCServer(('127.0.0.1', self.port))
        self.is_updating = True

        # ...................new fields.................#
        self.file_storage = []
        self.predecessor_node = ''
        self.FT_updater = ''
        # ..............................................#

        self.server.register_introspection_functions()
        self.server.register_function(self.get_finger_table)
        self.server.register_function(self.save_file)
        self.server.register_function(self.get_file)
        self.server.register_function(self.quit_p)

    def update_finger_table(self):
        while self.is_updating:
            time.sleep(1)
            if self.is_updating:
                self.populate_finger_table()

    def run(self):
        self.register()
        time.sleep(1)
        self.populate_finger_table()
        self.FT_updater = threading.Thread(target=self.update_finger_table)
        self.FT_updater.start()

        self.server.serve_forever()

    def register(self):
        self.proxy = ServerProxy('http://localhost:1000')
        self.id, msg = self.proxy.register(self.port)

    def populate_finger_table(self):
        random.seed(0)
        self.finger_table, self.predecessor_node = self.proxy.populate_finger_table(self.id)

    def get_finger_table(self):
        return self.finger_table

        # ........................................new methods....................................................#

    def save_file(self, file):
        if file not in self.file_storage:
            self.file_storage.append(file)
            return 'file stored in node ' + str(self.id)
        else:
            return 'file already exist stored in node ' + str(self.id)

    def get_file(self, file):
        if file in self.file_storage:
            return 'node ' + str(self.id) + ' has the file'
        else:
            return 'node ' + str(self.id) + 'does not have the file'

    def quit_p(self):
        print('quit')
        # check whether the node is part of the network
        if self.proxy.deregister(self.id):
            return 'Node ' + str(self.id) + ' with port ' + str(self.port) + ' was successfully removed'
        else:
            return 'Node ' + str(self.id) + ' with port ' + str(self.port) + ' was not a part of the system'
