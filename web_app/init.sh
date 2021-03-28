#!/bin/bash
# This script will replicate the python flask web app and setup the directory structure for each. It will also start up every instance of the app.

if [ $# != 1 ]; then
  echo "Error: Must provide number of web apps to spin up."
  echo "Standard form: $0 <num of instances>"
  exit
fi

# set run-time argument to num_instances variable
num_instances=$1

# set starting point for loop 
count=1

# set starting port for first web app instance
port=5001

# create working directory to house temporary intances of app and their logs:
mkdir working_dir

# loop and create new web app python script for number of instances provided
echo "Start: Creating $num_instances web app instance(s)"

while [ $count -le $num_instances ]; do
  echo "Creating web app $count, which will consume port $port"

  # create copy of python script, and move to working directory
  cp web_app.py working_dir/web_app_${count}.py

  # update port and instance number in newly copied script
  sed -i "s/REPLACE_WITH_PORT/${port}/g" working_dir/web_app_${count}.py
  sed -i "s/REPLACE_WITH_INSTANCE_NUMBER/${count}/g" working_dir/web_app_${count}.py

  echo "Starting new web app isntance"
  # startup new web app instance
  nohup working_dir/web_app_${count}.py > working_dir/web_app_${count}.log 2>&1 &

  # increment count and port values 
  count=$(( $count + 1 ))
  port=$(( $port + 1 ))
done


# check for running web app processes
echo "Init complete!"
echo "Currently running web app instances:"
ps -ef | grep web_app | grep -v grep


