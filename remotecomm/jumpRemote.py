#! /usr/bin/env python3
#################################################################################
#     File Name           :     remotecomm/jumpRemote.py
#     Created By          :     Eloi Silva (eloi@how2security.com.br)
#     Creation Date       :     [2017-07-13 15:51]
#     Last Modified       :     [2018-08-04 01:09]
#     Description         :     Version 1.0.0-dev1
#################################################################################

import sys, time, getpass
import pexpect
import remotecomm
from time import sleep
from getpass import getpass
from pexpect import TIMEOUT
from remotecomm.command import remoteCMD
from remotecomm.logbin import logbin

# Change the jump variable to correct ip address
jump = '200.204.1.12'
#jump = 'edit the variable jump into the remotecomm/jumpRemote file'

def jumpRemote(jump, username, password, host, *command, timeout=5.0, prompt_regex=None, logfile=None):
    log = logbin()
    conn = remoteCMD(jump, username, password)
    conn.jump()
    conn.remote(host, username, password)
    conn.connect.logfile_read = log
    try:
        for comm in command:
            conn.connect.sendline(comm)
            conn.prompt(timeout=timeout)
    except:
        print('[-] Router: %s' % host, end='')
    else:
        print('[+] Router: %s' % host, end='')
    finally:
        if not logfile:
            print(' Standard output...')
            sys.stdout.write(str(log))
        else:
            print(' File output[%s]' % logfile)
            with open(logfile, 'wb') as file:
                file.write(log.data)

def main():
    print('Jumpserver:', jump)
    host = input('Enter hostname: ')
    username = input('Enter username: ')
    password = getpass('Enter password: ')
    print('Enter commands, one per line. When done press dot(.)')
    command = []
    while True:
        comm = input('\tEnter command: ')
        if comm == '.': break
        else: command.append(comm)
    '''if 'exit' not in command or 'quit' not in command:
        command.append('exit')
        command.append('quit')
    '''
    jumpRemote(jump, username, password, host, *command)
    print()

if __name__ == '__main__':
    main()
