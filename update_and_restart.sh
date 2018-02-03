#!/bin/sh

# Commit changes with script comment
timestamp=`date "+%Y/%m/%d-%H:%M:%S"`
git add .
git commit -m "Script - ${timestamp}"
git push

# Create variables for SSH
pi_ip=$(cat pi_ip | grep "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*")
id_rsa=$(cat pi_ip | grep .ssh)
tbot=$(cat pi_ip | grep tbot)


# Query function for the RPi
do_query() {
    ssh -i ${id_rsa} pi@${pi_ip} $1 
}

# Create the query
query=(
    "cd ${tbot} && git pull && "                     # Pull changes on RPi
    "cat src/pid-bot | sudo xargs kill || true && "  # Stop (kill) last bot instance
    "cd src && sudo nohup ./run.py &!"               # Start a new bot instance
)

# Do the actual query
do_query "${query[*]}" 

echo "DONE"
