import fnmatch
import socket


def check_hostnames(switcher, value):
    hostname = socket.gethostname()
    return any(fnmatch.fnmatchcase(hostname, pattern) for pattern in value)
