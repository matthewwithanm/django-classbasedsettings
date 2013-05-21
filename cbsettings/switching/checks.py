import fnmatch
import os
import socket
import sys


def check_hostnames(switcher, value):
    hostname = socket.gethostname()
    return any(fnmatch.fnmatchcase(hostname, pattern) for pattern in value)


def check_testing(switcher, value):
    testing = len(sys.argv) >= 2 and [os.path.basename(sys.argv[0]),
                                      sys.argv[1]] == ['manage.py', 'test']
    return testing == value
