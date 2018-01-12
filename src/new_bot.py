#!/usr/bin/env pytho3.6

from telegram.ext import Updater, CommandHelper
from urllib.request import urlopen, URLError
import json, restrictions, sys, os, time
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
        

if __name__ == "__main__":
    token_file_path = os.path.join(DIR, '../token.json')
    try:
        with open(token_file_path) as file_o:
            secrets = json.load(file_o)
    except IOError:
        print("Could not find {}.".format(token_file_path)
        sys.exit(1)
    if 'token' not in secrets:
        print("E: no 'token' in {}".format(token_file_path))
        sys.exit(1)
    if 

