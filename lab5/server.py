from xmlrpc.server import SimpleXMLRPCServer
from Storage import Storage
import sys


def calculate(expression):
    try:
        print(expression)
        elements = (expression.split(' '))
        temp = elements[0]
        elements[0] = elements[1]
        elements[1] = temp
        print(eval(' '.join(elements)))
        return True, str(eval(' '.join(elements)))
    except ZeroDivisionError:
        print(f"{expression} -- not done")
        return False, "Division by zero"
    except (SyntaxError, ValueError):
        return False, "Logical error expression"
    except NameError:
        return False, "Write a math expression with numbers"


def main(argv):
    host = argv[0]
    port = int(argv[1])
    server = SimpleXMLRPCServer((host, port))
    print('Server is running...')
    server_storage = Storage('server')
    server.register_introspection_functions()
    server.register_function(calculate)
    server.register_instance(server_storage)
    server.serve_forever()


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Server is stopping')
        exit()
