from socket import socket, AF_INET, SOCK_DGRAM, timeout
from time import time
max_size = 1024


def process_first_message(recv_message: bytes, storage: dict):
    label, seq_no, extension, length = recv_message.decode().split("|")
    next_seq_no = int(seq_no) + 1
    length = int(length)
    if label == 's':
        storage['expected_size'] = length
        storage['expected_number_of_blocks'] = (length - 1) // (max_size - 16) + 1
        storage['next_seq_no'] = next_seq_no
        storage['extension'] = extension
        storage['last_reception'] = time()
        storage['data'] = []
        successful = True
    else:
        successful = False
    return successful, next_seq_no


def process_consecutive_message(recv_message: bytes, storage: dict):
    label, seq_no = recv_message[:15].decode().split("|")
    datagram = recv_message[16:]
    next_seq_no = int(seq_no) + 1
    if label == 'd' and storage['next_seq_no'] == int(seq_no):
        storage['data'].append(datagram)
        storage['next_seq_no'] = int(seq_no) + 1
        storage['last_reception'] = time()
        successful = True
        print(seq_no, " added")
    else:
        successful = False
    return successful, next_seq_no


def remove_old(storage: dict):
    current_time = time()
    addrs = list(storage.keys())
    for addr in addrs:
        if storage[addr]['expected_number_of_blocks'] == len(storage[addr]['data']) \
                and current_time - storage[addr]['last_reception'] > 1:
            del storage[addr]
            print(f'Data from {addr} removed')

        if current_time - storage[addr]['last_reception'] > 3:
            del storage[addr]
            print(f'Data from {addr} removed')

def main():
    storage = {}
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.bind(("localhost", 60001))
        s.settimeout(1.0)
        while True:
            remove_old(storage)
            try:
                recv_message, addr = s.recvfrom(100)
            except timeout:
                continue
            header = recv_message[:16].decode()
            if str(addr) not in storage.keys():
                storage[str(addr)] = {}
            if header.count("|") == 3:
                successful, next_seq_no = process_first_message(recv_message, storage[str(addr)])
                if successful:
                    message = f'a|{next_seq_no}|{max_size}'
                    s.sendto(message.encode(), addr)
            elif header.count("|") == 2:
                successful, next_seq_no = process_consecutive_message(recv_message, storage[str(addr)])
                if successful:
                    message = f'a|{next_seq_no}'
                    s.sendto(message.encode(), addr)
            else:
                raise ValueError("Expected three or four blocks in the message")
            remove_old(storage)

if __name__ == "__main__":
    main()
