import sys
import socket

HOST = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
PORT = int(sys.argv[2] if len(sys.argv) > 2 else 5555)

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))

s.listen(1)

while True:
    print(f'[*] listening as {HOST}:{PORT}')

    client = s.accept()
    print(f'[*] client connected {client[1]}')

    client[0].send('welcome to axju'.encode())
    while True:
        cmd = input('>>> ')
        client[0].send(cmd.encode())

        if cmd.lower() in ['q', 'quit', 'x', 'exit']:
            break

        result = client[0].recv(1024).decode()
        print(result)

    client[0].close()

    cmd = input('Wait for new client Y/n ') or 'y'
    if cmd.lower() in ['n', 'no']:
        break

s.close()
