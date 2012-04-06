import fnmatch
import socket


def check_hostnames(switcher, value):
    return socket.gethostname() in value
