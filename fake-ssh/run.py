#!/usr/bin/env python
import os
import logging
import socket
import sys
import threading

import paramiko

logging.basicConfig()
logger = logging.getLogger()

# if len(sys.argv) != 2:
#     print "Need private host RSA key as argument."
#     sys.exit(1)
#
host_key = paramiko.RSAKey(filename=os.path.join(os.path.dirname(__file__), "server_key"))


class Server(paramiko.ServerInterface):
    def __init__(self):
        print('init')
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        print('check_channel_request', kind, chanid)
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        print(username, password)
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        print('get_allowed_auths', username)
        return 'password'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True


def listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 2222))

    sock.listen(100)
    client, addr = sock.accept()

    t = paramiko.Transport(client)
    t.set_gss_host(socket.getfqdn(""))
    t.load_server_moduli()
    t.add_server_key(host_key)

    server = Server()
    t.start_server(server=server)

    # Wait 30 seconds for a command
    server.event.wait(30)
    t.close()


while True:
    try:
        listener()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        logger.error(exc)
