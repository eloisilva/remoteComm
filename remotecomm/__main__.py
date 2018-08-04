#! /usr/bin/env python3
#################################################################################
#     File Name           :     remotecomm/__main__.py
#     Created By          :     Eloi Silva (eloi@how2security.com.br)
#     Creation Date       :     [2017-07-13 18:16]
#     Last Modified       :     [2018-08-04 01:16]
#     Description         :     Version 1.0.0-dev1
#################################################################################

import sys, os, getpass, time
import threading, queue
import remotecomm
from time import sleep
from getpass import getpass
from remotecomm.jumpRemote import jumpRemote

# Change the jump variable to correct ip address
jump = '200.204.1.12'
#jump = 'edit the variable jump into the remotecomm/__main__ file'

# Debug configuration
debug = True
debug_dir = '/tmp/remotecomm/'

# How meny proccess (threds) simultaneous
threads = 10

# Routers
routers = sys.argv[1:]

# Queue and command variable
q = queue.Queue()
command = []

# Ask for username and password
print('Jumpserver: %s' % jump)
username = input('Enter username: ')
password = getpass('Enter password: ')

print('Enter commands, one per line. When done press dot(.)')
while True:
    comm = input('\tEnter command: ')
    if comm == '.': break
    else: command.append(comm)

print('\nCommand(s)')
for comm in command: print('\t%s' % comm)

print('\nRouters(s)')
for rtr in routers: print('\t%s' % rtr)

if input('\nContinue (y)es or (n)o: ') == 'n': 
    print('Exiting.')
    sys.exit(0)

class ExecRouter(threading.Thread):
    def __init__(self, q, tid):
        threading.Thread.__init__(self)
        self.tid = tid
        self.queue = q
    def run(self):
        print('Starting Thread-%s' % self.tid)
        while True:
            try:
                rtr = self.queue.get(timeout=5)
            except queue.Empty:
                print('Thread-%s: Done' % self.tid)
                return
            else:
                if not debug:
                    fileout = None
                else:
                    fileout = os.path.join(debug_dir, rtr + '_log.txt')
                jumpRemote(jump, username, password, rtr, *command, logfile=fileout)

def main():
    # Create the debug_dir if debug is True
    if debug:
        os.makedirs(debug_dir, exist_ok=True)
    # Add router to queue
    for router in routers:
        q.put(router)
    # Start threads
    for i in range(threads):
        th = ExecRouter(q, i)
        th.start()

if __name__ == '__main__':
    main()
