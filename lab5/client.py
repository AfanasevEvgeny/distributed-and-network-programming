import sys
from xmlrpc.client import ServerProxy
from Storage import Storage
import re


def main(argv):
    server_host = argv[0]
    server_port = int(argv[1])
    client_storage = Storage('client_storage')
    with ServerProxy(f'http://{server_host}:{server_port}', allow_none=True) as server:
        while True:
            print('enter the command:')
            command = str(input())
            if command =='quit' or 'send' or 'list' or 'delete' or 'get' or 'calc':
                try:
                    operation_type = command.split(' ')[0]
                    actions = command.split(' ', maxsplit=1)[1:]
                except IndexError:
                    print('Wrong command')
                if operation_type == 'quit':
                    print("Client is stopping")
                    exit()
                elif operation_type == 'send':
                    file_name = actions[0]
                    file = client_storage.get_file(file_name)
                    server.send_file(file_name, file)
                elif operation_type == 'list':
                    file_list = server.list_files()
                    print(file_list)
                elif operation_type == 'get':
                    file_name, local_filename = actions[0].split(' ')
                    client_storage.send_file(local_filename, server.get_file(file_name))
                elif operation_type == 'delete':
                    file_name = actions[0]
                    if not server.delete_file(file_name):
                        print('file is not in directory')
                    else:
                        print('file deleted')
                elif operation_type == 'calc':
                    expression = actions[0]
                    success, result = server.calculate(expression)
                    print(result)
                print('Command processed')

            else:
                print('Wrong command')


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Client is stopping')
        exit()
