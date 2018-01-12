#!/usr/bin/env python3.6

import json, requests, datetime, os
import run

run.wait_for_internet()

token    = json.load(open("../token.json"))["token"]
filename = 'update-' + str(datetime.datetime.now())
filepath = 'updates/' + filename

r = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(token))
get_json = r.json()

with open(filepath, 'w+') as output:
    json.dump(get_json, output, indent=4)

print("Created file: " + filename)

if not get_json['ok']:
    print('############################################')
    print('### WARNING: The return value was not OK ###')
    print('############################################')
elif len(get_json['result']) == 0:
    print('No new messages to report, automatic deletion')
    os.remove(filepath)


