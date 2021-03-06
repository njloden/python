import sys
import socket

"""
Author:         Nick Loden

Last Update:    03/06/2021

Description:    This script will provide a way to check a system and tcp port to determine if a connection can be made. 

Input:          hostname/IPv4 address & tcp port 

Standard Form:  import tcp_test
                tcp_test.check_port(server.example.com, 80)

"""


def check_port(host, port):
    """returns true if a connection can be made with the provided host and port"""
    timeout = 1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        s.connect((host, port))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()


