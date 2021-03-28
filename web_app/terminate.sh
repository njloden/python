#!/bin/bash
# Note: Need to run as sudo as the working dir and processes were created via sudo or root
# Standard Form: sudo ./terminate.sh

# search for and terminate currently running web app processes
ps -ef | grep web_app_ | grep -v grep | awk '{print $2}' | xargs kill -9

# purge temporary working directory
rm -rf working_dir


