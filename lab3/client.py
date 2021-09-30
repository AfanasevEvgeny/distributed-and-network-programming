from socket import socket, AF_INET, SOCK_DGRAM, timeout


def send_message_5trials(send_datagram: bytes, socket_: socket):
    """
    :param socket_:
    :param send_datagram:
    :return:
    """
    timeouts = 0
    recv_datagram = None
    for i in range(5):
        try:
            socket_.sendto(send_datagram, ("localhost", 60001))
            print(f"Sent: {send_datagram}")
            recv_datagram, _ = socket_.recvfrom(1024)
            print(f"Received: {recv_datagram.decode()}")
            break
        except timeout:
            timeouts += 1

    successful = timeouts != 5
    if successful:
        recv_datagram = recv_datagram.decode()
    return successful, recv_datagram


def split_data(data, maxsize):
    """
    :param data:
    :param maxsize:
    """
    datagrams = []
    n_grams = (len(data) - 1) // maxsize + 1
    for i in range(n_grams):
        datagrams.append(data[i * maxsize: (i + 1) * maxsize])
    return datagrams


def main():
    """
    Main function
    """
    with open('innopolis.jpg', 'rb') as file:
        data = file.read()
    with socket(AF_INET, SOCK_DGRAM) as s:
        s.bind(("localhost", 60000))
        s.settimeout(0.5)
        # message passing initialization
        send_message = 's|000000000|jpg|' + str(len(data))
        success, recv_message = send_message_5trials(send_message.encode(), s)
        if not success:
            exit(0)

        # data preparation
        ack, seq_no, maxsize = recv_message.split('|')
        seq_no, maxsize = int(seq_no), int(maxsize)

        # data transmission
        if ack == 'a':
            # 9 bytes are reserved for the message header
            datagrams = split_data(data, maxsize - 9)
            for i, datagram in enumerate(datagrams):
                send_message = 'd|{:013d}|'.format(i + 1).encode() + datagram
                success, recv_message = send_message_5trials(send_message, s)
                if not success:
                    exit(0)


if __name__ == '__main__':
    main()
