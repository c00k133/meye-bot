#!/usr/bin/env python3.6

import socket, os

pid = os.getpid()
print("PID: {}".format(pid))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 9988))
s.listen(1)

def func(data):
    print(data)

while True:
    conn, addr = s.accept()
    data = conn.recv(1024)
    conn.close()
    func(data)

