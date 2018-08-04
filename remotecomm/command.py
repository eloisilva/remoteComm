#! /usr/bin/env python
#################################################################################
#     File Name           :     command.py
#     Created By          :     Eloi Silva (eloi@how2security.com.br)
#     Creation Date       :     [2017-05-23 01:18]
#     Last Modified       :     [2018-08-04 00:42]
#     Description         :     
#################################################################################

import sys
import time
import pexpect

class remoteCMD:
    def __init__(self, hostname, username, password, prompt_regex=None, timeout=5.0):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.prompt_regex = '.*$|.*#' if not prompt_regex else prompt_regex
        self.prompt_exact = ''

    def jump(self):
        self.connect = pexpect.spawn('ssh %s@%s' % (self.username, self.hostname), maxread=500000)
        result = self.connect.expect(['[p|P]assword', '(yes/no)'], timeout=self.timeout)
        if result == 1:
            self.connect.sendline('yes')
            self.connect.expect('[p|P]assword')
        self.connect.sendline(self.password)
        if self.prompt_guess():
            self.prompt_regex = None

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
        if self.prompt_guess():
            self.prompt_regex = None

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

    def prompt_expect(self, timeout=None):
        timeout = timeout or self.timeout
        if self.prompt_exact:
            self.connect.expect_exact(self.prompt_exact, timeout=timeout)
        elif self.prompt_regex:
            self.connect.expect(self.prompt_regex, timeout=timeout)
        else:
            raise pexpect.TIMEOUT

    def prompt(self, **kargs):
        try:
            self.prompt_expect(**kargs)
        except pexpect.TIMEOUT:
            try:
                self.prompt_guess()
                self.connect.sendline()
                self.prompt_expect()
            except:
                sys.stderr.write('Error trying to expect device prompt')

    def __del__(self):
        if self.connect.terminate():
            print('Session ended')
