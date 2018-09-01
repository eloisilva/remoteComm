#! /usr/bin/env python3
#################################################################################
#     File Name           :     remotecomm/__main__.py
#     Created By          :     Eloi Silva (eloi@how2security.com.br)
#     Creation Date       :     [2017-07-13 18:16]
#     Last Modified       :     [2018-09-01 00:58]
#     Description         :     Version 1.0.3-dev1
#################################################################################

import sys, os, getpass, time
import threading, queue
import argparse
import remotecomm
from time import sleep
from getpass import getpass
from remotecomm.jumpRemote import jumpRemote
from remotecomm.ipv4 import ip_check

# Creating a parser arguments
parser = argparse.ArgumentParser()

# Pass a file to read commands
parser.add_argument('-f', '--file',
        help='File with routers commands. One command per line. Commands will be asked it file not given.',
        type=argparse.FileType('r'),
        metavar='filename',
        dest='commands',
        required=False
        )

# Jumpserver
parser.add_argument('-j', '--jump',
        help='Jumpserver name or ip address.',
        metavar='host',
        dest='jump',
        required=True
        )

# routers
parser.add_argument('routers',
        help='Routers should be separeted by space.',
        nargs='+'
        )

# How many threads
parser.add_argument('-t', '--threads',
        help='How many threads.',
        type=int,
        default=10,
        metavar='n',
        dest='threads',
        required=False
        )

# Timeout
parser.add_argument('--timeout',
        help='Prompt expect timeout',
        type=int,
        default=5,
        metavar='n',
        dest='timeout',
        required=False
        )

# Debug
parser.add_argument('--debug',
        help='Enable debug mode.',
        action='store_true',
        default=False,
        dest='debug'
        )

# Output to stdout or directory
parser.add_argument('--stdout',
        help='Send output to stdout. If not given, the output will be send to directory.',
        action='store_true',
        default=False,
        dest='screen'
        )

parser.add_argument('--dirout',
        dest='dirout',
        metavar='dirpath',
        default='/tmp/remotecomm',
        help='Specify diretory path output (Default: /tmp/remotecomm).'
        )

class Config:
    def __init__(self, parser):
        self.args = parser.parse_args()
        self.queue = queue.Queue()
        self.screen = self.arg_screen
        self.debug = self.args.debug
        self.jump = self.args.jump
        self.commands = self.arg_commands
        self.routers = self.arg_routers
        self.threads = self.args.threads
        self.timeout = self.args.timeout

    @property
    def arg_screen(self):
        # Create the output_dir if terminal is False
        if self.args.screen:
            return self.args.screen
        else:
            try:
                os.makedirs(self.args.dirout, exist_ok=True)
            except Exception:
                sys.stderr.write('Permission Error to create directory: %s' % self.args.dirout)
                sys.exit(1)
            else:
                return self.args.dirout

    @property
    def arg_commands(self):
        if self.args.commands:
            return [comm.strip() for comm in self.args.commands]
        else:
            commands = []
            print('Enter commands, one per line. When done press dot(.)')
            while True:
                comm = input('\tEnter command: ')
                if comm == '.': break
                else: commands.append(comm)
            return commands

    @property
    def arg_routers(self):
        return [router.strip().lower() for router in self.args.routers]

    def show_info(self, kargs):
        for key in kargs:
            print('\n%s(s)' % key)
            for item in kargs[key]:
                print('\t%s' % item)

    def run(self):
        # Show routers
        self.show_info({'Router': self.routers})

        # Show commands
        self.show_info({'Command': self.commands})

        # Config exec
        if input('\nContinue (y)es or (n)o: ') == 'n': 
            print('Exiting.')
            sys.exit(0)

        # Ask for username and password
        print('Jumpserver: %s' % self.jump)
        username = input('Enter username: ')
        password = getpass('Enter password: ')

        # Add router to queue
        for router in self.routers:
            self.queue.put(router)
        # Start threads
        for ti in range(self.threads):
            th = ExecRouter(self.queue, ti, self.jump, username, password, self.commands, self.screen, self.timeout, self.debug)
            th.start()

class ExecRouter(threading.Thread):
    def __init__(self, q, tid, jump, username, password, commands, screen, timeout, debug):
        threading.Thread.__init__(self)
        self.tid = tid
        self.queue = q
        self.jump = jump
        self.username = username
        self.password = password
        self.commands = commands
        self.screen = screen
        self.debug = debug
        self.timeout = timeout
    def run(self):
        print('Starting Thread-%s' % self.tid)
        while True:
            try:
                rtr = self.queue.get(timeout=5)
            except queue.Empty:
                print('Thread-%s: Done' % self.tid)
                return
            else:
                if self.screen == True:
                    fileout = None
                else:
                    fileout = os.path.join(self.screen, rtr + '_log.txt')
                jumpRemote(self.jump, self.username, self.password, rtr, *self.commands, logfile=fileout, timeout=self.timeout, debug=self.debug)

def main():
    config = Config(parser)
    config.run()

if __name__ == '__main__':
    main()
