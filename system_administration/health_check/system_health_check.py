import socket
import psutil
import time

"""
Author:         Nick Loden

Last Update:    02/06/2021

Description:    This script will provide basic system information and utilization statistics that one could use
                to determine the overall health of said system.

Input:          None

Standard Form:  python system_health_check.py

Installation/Configuration Guidance:

    Option 1:
        pip install -r requirements.txt

    Option 2:
        pip install psutil
"""


def get_hostname():
    """returns hostname of system."""
    return socket.gethostname()


def get_boot_time():
    """returns boot time of system."""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))


def get_core_counts():
    """returns physical and logical core count of cpu."""
    physical_count = psutil.cpu_count(logical=False)
    logical_count = psutil.cpu_count(logical=True)
    return physical_count, logical_count


def get_cpu_util(poll_time=1):
    """returns current cpu utilization."""
    return psutil.cpu_percent(poll_time)


def get_cpu_load_avg():
    """returns 1, 5, and 15 min cpu load averages."""
    one, five, fifteen = psutil.getloadavg()
    return one, five, fifteen


def get_memory_util():
    """returns current memory utilization."""
    current_memory_stats = psutil.virtual_memory()
    total_mem = current_memory_stats[0]
    avail_mem = current_memory_stats[1]
    percent_used_mem = current_memory_stats[2]

    # convert bytes to GB
    total_mem_gb = int(total_mem) / 1000000000
    avail_mem_gb = int(avail_mem) / 1000000000

    return total_mem_gb, avail_mem_gb, percent_used_mem


def get_swap_util():
    """returns current swap memory utilization."""
    current_swap_stats = psutil.swap_memory()
    total_swap = current_swap_stats[0]
    avail_swap = current_swap_stats[2]
    percent_used_swap = current_swap_stats[3]

    # convert bytes to GB
    total_swap_gb = int(total_swap) / 1000000000
    avail_swap_gb = int(avail_swap) / 1000000000

    return total_swap_gb, avail_swap_gb, percent_used_swap


def get_network_interfaces():
    """returns list of network interfaces."""
    interfaces = []
    for interface in psutil.net_if_addrs().keys():
        interfaces.append(interface)
    return interfaces


def get_active_users():
    """returns list of users currently logged into system."""
    user_list = []
    for user in psutil.users():
        user_list.append(user[0])
    return user_list


def get_disk_util():
    """returns list of all mounted disk partitions and their utilization."""
    disk_partitions = {}

    # find all mounted disk partitions on system
    for partition in psutil.disk_partitions():
        try:
            # extract second element in tuple and set as mount_point value
            mount_point = partition[1]

            # pull disk statistics from current mount point
            disk_total, disk_used, disk_free, disk_percent_used = psutil.disk_usage(mount_point)

            # convert bytes to GB
            disk_total_gb = int(disk_total) / 1000000000
            disk_free_gb = int(disk_free) / 1000000000

            # add current partition name (key) and stats as list (value) to return dictionary
            disk_partitions[mount_point] = [disk_total_gb, disk_free_gb, disk_percent_used]
        except Exception:  # if cannot access partition, continue on
            pass

    return disk_partitions


def health_check():
    """combine health check functions and output results"""
    # call other functions and assign return values to local variables
    hostname = get_hostname()
    boot_time = get_boot_time()
    physical_cores, logical_cores = get_core_counts()
    network_interfaces = get_network_interfaces()
    cpu_util = get_cpu_util()
    one, five, fifteen = get_cpu_load_avg()
    total_mem, avail_mem, percent_used_mem = get_memory_util()
    total_swap, avail_swap, percent_used_swap = get_swap_util()
    disk_partition_dict = get_disk_util()
    active_user_list = get_active_users()

    # print output
    print(' -------------')
    print('| System Info |')
    print(' -------------')
    print('Hostname: {}'.format(hostname))
    print('Boot Time: {}'.format(boot_time))
    print('CPU: Physical Cores: {} | Logical Cores: {}'.format(physical_cores, logical_cores))
    print('Network Interfaces: {}'.format(', '.join(network_interfaces)))
    print('')

    print(' -----')
    print('| CPU |')
    print(' -----')
    print('Current system wide CPU utilization: {}%'.format(cpu_util))
    print('1, 5, and 15 min CPU load averages: {}%, {}%, {}%'.format(one, five, fifteen))
    print('')

    print(' --------')
    print('| Memory |')
    print(' --------')
    print('Total: {:.2f} GB | Available: {:.2f} GB | Used: {} %'.format(total_mem, avail_mem, percent_used_mem))
    print('')

    print(' ------------')
    print('| Swap Space |')
    print(' ------------')
    print('Total: {:.2f} GB | Available: {:.2f} GB | Used: {} %'.format(total_swap, avail_swap, percent_used_swap))
    print('')

    print(' ------')
    print('| Disk |')
    print(' ------')
    for disk_partion, disk_stats in disk_partition_dict.items():
        print('Partition: {}'.format(disk_partion))
        print('Total Size: {:.2f} GB | Disk Free: {:.2f} GB | Used: {} %'.format(disk_stats[0], disk_stats[1], disk_stats[2]))
        print('')
    print('')

    print(' --------------')
    print('| Active Users |')
    print(' --------------')
    print(', '.join(active_user_list))


if __name__ == '__main__':
    health_check()