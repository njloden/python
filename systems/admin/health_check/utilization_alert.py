import shutil
import psutil
import socket

"""
Author:         Nick Loden

Last Update:    02/27/2021

Description:    This script will check several resources on the system and generate an alert if a utilization threshold
                has been exceeded.

Input:          None

Standard Form:  python utilization_alert.py

Installation/Configuration Guidance:

    Option 1:
        pip install -r requirements.txt

    Option 2:
        pip install psutil
"""


issues = []


def check_cpu():
    """returns True if the current cpu utilization is below 80%"""
    usage = psutil.cpu_percent(1)
    return usage < 80


def check_disk():
    """returns True if the root file system has greater than 20% of available disk space"""
    du = shutil.disk_usage('/')
    free = du.free / du.total * 100
    return free > 20


def check_mem():
    """returns True if the amount of available memory is greater than 500 MB"""
    mem = psutil.virtual_memory()
    available = mem.available / 1000000
    return available > 500


def check_localhost():
    """returns True if localhost can be resolved and return local loopback address"""
    localhost = socket.gethostbyname('localhost')
    return localhost == '127.0.0.1'


if __name__ == '__main__':
    if not check_cpu():
        issues.append('CPU usages is over 80%')

    if not check_disk():
        issues.append('Available disk space of root volume is less than 20%')

    if not check_mem():
        issues.append('Available memory is less than 500 MB')

    if not check_localhost():
        issues.append('Localhost cannot be resolved')

    if issues:
        for issue in issues:
            print('Error: {}'.format(issue))


