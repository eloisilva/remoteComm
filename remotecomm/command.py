#! /usr/bin/env python
#################################################################################
#     File Name           :     command.py
#     Created By          :     Eloi Silva (eloi@how2security.com.br)
#     Creation Date       :     [2017-05-23 01:18]
#     Last Modified       :     [2018-07-28 04:22]
#     Description         :     
#################################################################################

import time
import pexpect
from pexpect import TIMEOUT

class remoteCMD:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.prompt_regex = '.*$|.*#'

    def jump(self):
        self.connect = pexpect.spawn('ssh %s@%s' % (self.username, self.hostname), maxread=500000)
        result = self.connect.expect(['[p|P]assword', '(yes/no)'])
        if result == 1:
            self.connect.sendline('yes')
            self.connect.expect('[p|P]assword')
        self.connect.sendline(self.password)
        self.connect.expect(self.prompt_regex)
        #self.prompt_guess()
        #self.prompt()

    def remote(self, hostname, username, password):
        self.prompt_regex = '.*$|.*#|.*>'
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
        self.connect.expect(self.prompt_regex)
        #self.prompt_guess()
        #self.prompt()

    def prompt_get(self, timeout=0.1, total_timeout=5.0):
        # Create the prompt
        prompt = self.connect.string_type()
        start = time.time()
        wait = 0.0

        # Try to get the prompt in the max of total_timeout and return it
        while wait < total_timeout:
            try:
                prompt += self.connect.read_nonblocking(size=1, timeout=timeout)
                wait = time.time() - start
            except TIMEOUT:
                break
        return prompt

    def prompt_guess(self, **kargs):
        # Discard first prompt
        self.connect.sendline()
        try:
            self.prompt_get(**kargs)
        except TIMEOUT:
            pass

        # First prompt
        self.connect.sendline()
        prompt_guess_1 = self.prompt_get(**kargs)

        # Second prompt
        self.connect.sendline()
        prompt_guess_2 = self.prompt_get(**kargs)

        # Compare prompts and return it if match
        if prompt_guess_1 == prompt_guess_2:
            self.prompt_exact = prompt_guess_1
        else:
            self.prompt_exact = False

    def prompt(self):
        if self.prompt_exact:
            self.connect.expect_exact(self.prompt_exact)
        else:
            self.connect.expect(self.prompt_regex)

