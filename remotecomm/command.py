#! /usr/bin/env python
#################################################################################
#     File Name           :     command.py
#     Created By          :     Eloi Silva (eloi@how2security.com.br)
#     Creation Date       :     [2017-05-23 01:18]
#     Last Modified       :     [2018-08-03 20:06]
#     Description         :     
#################################################################################

import time
import pexpect
#from pexpect import TIMEOUT

class remoteCMD:
    def __init__(self, hostname, username, password, timeout=5.0):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.prompt_regex = '.*$|.*#'
        self.prompt_exact = ''

    def jump(self):
        self.connect = pexpect.spawn('ssh %s@%s' % (self.username, self.hostname), maxread=500000)
        result = self.connect.expect(['[p|P]assword', '(yes/no)'], timeout=self.timeout)
        if result == 1:
            self.connect.sendline('yes')
            self.connect.expect('[p|P]assword')
        self.connect.sendline(self.password)
        self.prompt_guess()

    def remote(self, hostname, username, password):
        self.prompt_regex = '.*$|.*#|.*>'
        comm_ssh = 'ssh %s@%s' % (username, hostname)
        self.connect.sendline(comm_ssh)
        result = self.connect.expect(['[p|P]assword', pexpect.TIMEOUT], timeout=self.timeout)
        if result == 1:
            comm_telnet = 'telnet %s' % (hostname)
            self.connect.sendline(comm_telnet)
            self.connect.expect('[u|U]sername')
            self.connect.sendline(username)
            self.connect.expect('[p|P]assword')
        self.connect.sendline(password)
        self.prompt_guess()

    def timeout_set(x):
        try:
            timeout = float(x)
            self.timeout = timeout
        except:
            print('Error trying to set timeout, make sure you are gave a number as timeout argument')

    def prompt_get(self, timeout_char=0.1):
        # Create the prompt
        prompt = self.connect.string_type()
        start = time.time()
        wait = 0.0

        # Try to get the prompt in the max of prompt_timeout and return it
        while wait < self.timeout:
            try:
                prompt += self.connect.read_nonblocking(size=1, timeout=timeout_char)
                wait = time.time() - start
            except pexpect.TIMEOUT:
                break
        return prompt

    def prompt_guess(self, **kargs):
        # Discard first prompt
        self.connect.sendline()
        try:
            self.prompt_get(**kargs)
        except pexpect.TIMEOUT:
            pass

        # Start time
        start = time.time()
        wait = 0.0

        while wait < self.timeout:
            # First prompt
            self.connect.sendline()
            prompt_guess_1 = self.prompt_get(**kargs)

            # Second prompt
            self.connect.sendline()
            prompt_guess_2 = self.prompt_get(**kargs)

            # Compare prompts and return it if match
            if prompt_guess_1 == prompt_guess_2 and len(prompt_guess_1) > 4:
                self.prompt_exact = prompt_guess_1
                return True
            else:
                self.prompt_exact = ''
            wait = time.time() - start

    def prompt_expect(self):
        if self.prompt_exact:
            self.connect.expect_exact(self.prompt_exact, timeout=self.timeout)
        else:
            self.connect.expect(self.prompt_regex, timeout=self.timeout)

    def prompt(self, **kargs):
        try:
            self.prompt_expect()
        except pexpect.TIMEOUT:
            self.prompt_guess(**kargs)
            self.connect.sendline()
            self.prompt_expect()
