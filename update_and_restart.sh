#!/bin/sh

# Commit changes with script comment
timestamp=`date "+%Y/%m/%d-%H:%M:%S"`
git add .
git commit -m "Script - ${timestamp}"
git push

# Create variables for SSH
pi_ip=$(cat pi_ip | grep 192)
id_rsa=$(cat pi_ip | grep .ssh)
tbot=$(cat pi_ip | grep tbot)
query="cd ${tbot} && git pull"

# Query function for the RPi
do_query() {
    ssh -i ${id_rsa} pi@${pi_ip} $1
}

# Pull changes on RPi
#ssh -i ${id_rsa} pi@${pi_ip} ${query}
do_query "cd ${tbot} && git pull"

# Report if success or not
if [[ $? -eq 0 ]]; then
    echo "Success"
else
    echo "Failed"
fi

# Restart the bot
do_query "cat ${tbot}/src/pid-bot | kill -l"
do_query "cd ${tbot}/src && nohup ./run.py &!"

