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

# Pull changes on RPi
ssh -i ${id_rsa} pi@${pi_ip} 'cd ${tbot} && git pull'

if [[ $? -eq 0 ]]; then
    echo "Success"
else
    echo "Failed"
fi

