#! /usr/bin/env python3
#################################################################################
#     File Name           :     remotecomm/ha.py
#     Created By          :     Eloi Silva (eloi@how2security.com.br)
#     Creation Date       :     [2017-07-13 18:16]
#     Last Modified       :     [2018-11-18 23:21]
#     Description         :     Version 1.0.1-dev1
#################################################################################

import sys, os, getpass, time, base64, threading
from time import sleep
from random import randint
from getpass import getpass
from remotecomm.command import remoteCMD
from remotecomm.ipv4 import is_ipv4

# Test User (Fake password)
def info_socrbash(qnt, jump, sessions):
    jump = '127.0.0.1'
    username = 'soc_rbash'
    password = base64.b64decode(b'6675636b2070617373776f7264').decode('utf-8')
    return [remoteCMD, [jump, username, password], sessions, qnt]

class connect(threading.Thread):
    def __init__(self, cls, info, sessions, qnt):
        threading.Thread.__init__(self)
        self.cls = cls
        self.info = info
        self.qnt = qnt
        self.sessions = sessions

    def run(self):
        for i in range(self.qnt):
            self.s = self.cls(*self.info)
            self.s.jump()
            self.gethost()
            if is_ipv4(self.host):
                try:
                    self.s.remote(self.host, self.info[1], self.info[2])
                    self.s.prompt()
                except:
                    pass
            self.sessions.append(self.s)

    def gethost(self):
        hostline = randint(1,41000)
        cmd = "sed -n '%s,$p' /etc/hosts |grep -i 'i-br\|c-br' |head -1 |awk '{print $1}'" % hostline
        self.s.connect.sendline(cmd)
        self.s.prompt()
        self.host = self.s.connect.before.decode().rstrip().split()[-1]
        
def conn(qnt, *args):
    ths = []
    for i in range(qnt):
        th = connect(*args)
        th.start()
        ths.append(th)
    return(ths)

if __name__ == '__main__':
    '''
    soc = info_socrbash(2, jump, [])
    threads = conn(10, *soc)
    '''
    # Session users from soc_rbash1 to soc_rbash100
    def open_sessions(qnt, sessions, start=1, stop=101):
        jump = '127.0.0.1'
        threads = []
        username = 'soc_rbash'
        password = base64.b64decode(b'6675636b2070617373776f7264').decode('utf-8')
        for i in range(start,stop):
            user = username+str(i)
            threads += conn(1, *[remoteCMD, [jump, user, password], sessions, qnt])
        return threads

    def quit_sessions(sessions):
        getpass('Press Enter to start quit sessions...')
        for s in sessions: s.connect.sendline('exit')

    sessions = []
    threads = []
    print('Starting first burst: users from 1 to 50')
    threads += open_sessions(3, sessions, start=1, stop=51)
    time.sleep(10)
    for th in threads: th.join()
    print('Starting second burst: users from 51 to 100')
    threads += open_sessions(3, sessions, start=51, stop=101)
    time.sleep(10)
    for th in threads: th.join()
    print('Starting third burst: users from 101 to 150')
    threads += open_sessions(3, sessions, start=101, stop=151)
    time.sleep(10)
    for th in threads: th.join()
    print('Starting fourth burst: users from 151 to 200')
    threads += open_sessions(3, sessions, start=151, stop=201)
    time.sleep(10)
    for th in threads: th.join()
    print('Starting fiveth burst: users from 201 to 250')
    threads += open_sessions(3, sessions, start=201, stop=251)
    time.sleep(10)
    for th in threads: th.join()
    print('Starting sixth burst: users from 251 to 300')
    threads += open_sessions(3, sessions, start=251, stop=301)
    time.sleep(10)
    for th in threads: th.join()
    quit_sessions(sessions)
