import os
import tcp_test

"""
Author:         Nick Loden

Last Update:    03/06/2021

Description:    This script will consume a dictionary containing a host or hosts with their associated services and ports. For each service
                and port, the tcp_test.check_port() fucntion will be called to see if the service is online or not. After the status is captured,
                the results will be written in html format to the output file specified.

Input:          None

Standard Form:  python gen_html_report.py

"""


output_file = '/var/www/html/service_status.html'
online_str = '<p style="color:green">Online</p>'
offline_str = '<p style="color:red">Offline</p>'

test_app = {'127.0.0.1': {'apache': 80, 'tomcat': 8080},
            'localhost': {'apache2': 80}  
           }


def check_app(servers):
    """returns the status of every service provided (online or offline) in html format"""
    tmp_str = ''

    for host, services in servers.items():
        counter = 0
        for service, port in services.items():
            result = tcp_test.check_port(host, port)

            if result:
                status = online_str
            else:
                status = offline_str

            if counter == 0:
                tmp_str += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td>'.format(host, service, port, status)
            else:
                tmp_str += '<tr><td></td><td>{}</td><td>{}</td><td>{}</td>'.format(service, port, status)
            counter += 1

    return tmp_str 


def print_header():
    return '<html><table border="1"><tr><th>Server</th><th>Service</th><th>Port</th><th>Status</th></tr>'


def print_footer():
    return '</table></html>'


if __name__ == '__main__':
    html_str = print_header()
    html_str += check_app(test_app)
    html_str += print_footer()

    with open(output_file, 'w') as f:
        f.write(html_str)

