import json, requests, datetime, os

token    = json.load(open("../../token.json.json"))["token.json"]
filename = 'update-' + str(datetime.datetime.now())
filepath = 'updates/' + filename

r = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(token))
get_json = r.json()

with open(filepath, 'w+') as output:
    json.dump(get_json, output, indent=4)

print("Created file: " + filename)

if not get_json['ok']:
    print('###################################################')
    print('### WARNING: The return return value was not OK ###')
    print('###################################################')
elif len(get_json['result']) == 0:
    print('No new messages to report, automatic deletion')
    os.remove(filepath)


