#!/usr/bin/env python3.6

import socket, os

print("PID: {}".format(os.getpid()))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9988))
s.sendall(b'Something moved!')
s.close()

