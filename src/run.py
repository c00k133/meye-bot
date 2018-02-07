#!/usr/bin/env python3.6

from urllib.request import urlopen, URLError
import json, sys, os, time, socket
import bot

DIR = os.path.dirname(__file__)

def check_connectivity(reference):
    try:
        urlopen(reference, timeout=1)
        return True
    except URLError:
        return False

def wait_for_internet():
    while not check_connectivity('https://api.telegram.org'):
        print('Waiting for internet')
        time.sleep(1)

def save_pid():
    pid = str(os.getpid())
    with open('pid-bot', 'w+') as pid_f:
        pid_f.write(pid)

def parse(data, a):
    a.test_listen(data.decode('utf-8'))

def listen(a):
    print("Started listening")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 9988))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        conn.close()
        parse(data, a)
        

if __name__ == "__main__":
    save_pid()

    token_file_path = os.path.join(DIR, '../token.json')
    try:
        with open(token_file_path) as file_o:
            secrets = json.load(file_o)
    except IOError:
        print("Could not find {}.".format(token_file_path))
        sys.exit(1)
    if 'token' not in secrets:
        print("E: no 'token.json' in {}".format(token_file_path))
        sys.exit(1)
    if 'auth_check' not in secrets:
        print("E: no 'admins' in {}".format(token_file_path))
        sys.exit(1)
    name = None
    if 'name' in secrets:
        name = secrets['name']

    for user in secrets['auth_check']:
        bot.LIST_OF_USERS.append(user['id'])
        bot.MAC_ADDRESSES.update({user['mac'] : user['username']})
        if user['admin']:
            bot.TEST_USERS.append(user['id'])

    wait_for_internet()

    a = bot.Bot(secrets['token'], name=name)
    try:
        print('Starting bot')
        a.run()
        listen(a)
    except KeyboardInterrupt:
        print('W: interrupt received, stopping... (this might take some seconds)')
        a.stop()

