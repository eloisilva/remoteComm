#! /usr/bin/env python
#################################################################################
#     File Name           :     command.py
#     Created By          :     Eloi Silva (eloi@how2security.com.br)
#     Creation Date       :     [2017-05-23 01:18]
#     Last Modified       :     [2018-07-25 18:25]
#     Description         :     
#################################################################################

import pexpect

class remoteCMD:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def jump(self):
        prompt = '.*$|.*#'
        self.connect = pexpect.spawn('ssh %s@%s' % (self.username, self.hostname), maxread=500000)
        result = self.connect.expect(['[p|P]assword', '(yes/no)'])
        if result == 1:
            self.connect.sendline('yes')
            self.connect.expect('[p|P]assword')
        self.connect.sendline(self.password)
        self.connect.expect(prompt)

    def remote(self, hostname, username, password):
        rtr_prompt = '.*$|.*#|.*>'
        comm_ssh = 'ssh %s@%s' % (username, hostname)
        comm_telnet = 'telnet %s' % (hostname)
        self.connect.sendline(comm_ssh)
        result = self.connect.expect(['[p|P]assword', pexpect.TIMEOUT], timeout=10)
        if result == 1:
            self.connect.sendline(comm_telnet)
            self.connect.expect('[u|U]sername')
            self.connect.sendline(username)
            self.connect.expect('[p|P]assword')
            self.connect.sendline(password)
        elif result == 0:
            self.connect.sendline(password)
        self.connect.expect(rtr_prompt)
