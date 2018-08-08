#! /usr/bin/env python
#################################################################################
#     File Name           :     command.py
#     Created By          :     Eloi Silva (eloi@how2security.com.br)
#     Creation Date       :     [2017-05-23 01:18]
#     Last Modified       :     [2018-08-08 20:47]
#     Description         :     
#################################################################################

import sys
import time
import pexpect

class remoteCMD:
    def __init__(self, hostname, username, password, timeout=10.0, prompt_regex='', debug=True):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.debug = debug
        self.prompt_regex = prompt_regex
        self.prompt_exact = ''

    def jump(self):
        if self.debug: print('Method self.jump')
        self.connect = pexpect.spawn('ssh %s@%s' % (self.username, self.hostname), maxread=500000)
        result = self.connect.expect(['[p|P]assword', '(yes/no)'], timeout=self.timeout)
        if result == 1:
            self.connect.sendline('yes')
            self.connect.expect('[p|P]assword')
        self.connect.sendline(self.password)
        self.prompt()

    def remote(self, hostname, username, password):
        if self.debug: print('Method self.remote')
        self.prompt_exact = ''
        comm_ssh = 'ssh %s@%s' % (username, hostname)
        self.connect.sendline(comm_ssh)
        try:
            self.connect.expect('[p|P]assword', timeout=self.timeout)
        except pexpect.TIMEOUT:
            comm_telnet = 'telnet %s' % (hostname)
            self.connect.sendline(comm_telnet)
            self.connect.expect('[u|U]sername')
            self.connect.sendline(username)
            self.connect.expect('[p|P]assword')
        finally:
            self.connect.sendline(password)
            self.prompt()

    def timeout_set(x):
        if self.debug: print('Method timeout_set')
        try:
            timeout = float(x)
            self.timeout = timeout
        except:
            print('Error trying to set timeout, make sure you are gave a number as timeout argument')

    def prompt_get(self, timeout_char=0.1):
        if self.debug: print('Method self.prompt_get')
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
        if self.debug: print('Method self.prompt_guess')
        # Discard first prompt
        try:
            self.connect.sendline()
            self.prompt_get(**kargs)
        except pexpect.TIMEOUT:
            pass

        # Start time
        start = time.time()
        wait = 0.0
        try_count = 1

        while wait < self.timeout:
            if self.debug: print('try - %d' % try_count)
            # First prompt
            self.connect.sendline()
            prompt_guess_1 = self.prompt_get(**kargs)

            # Second prompt
            self.connect.sendline()
            prompt_guess_2 = self.prompt_get(**kargs)

            # Compare prompts and return it if match
            if prompt_guess_1 == prompt_guess_2 and len(prompt_guess_1) > 4:
                if self.debug: print('prompt found')
                self.prompt_exact = prompt_guess_1
                return True
            else:
                if self.debug: print('prompt not found')
                self.prompt_exact = ''
            try_count += 1
            wait = time.time() - start

    def prompt_expect(self, timeout=None):
        if self.debug: print('Method self.prompt_expect', end=': ')
        timeout = timeout or self.timeout
        if self.prompt_exact:
            if self.debug: print('expecting prompt %s' % self.prompt_exact)
            self.connect.expect_exact(self.prompt_exact, timeout=timeout)
        elif self.prompt_regex:
            if self.debug: print('expecting prompt %s' % self.prompt_regex)
            self.connect.expect(self.prompt_regex, timeout=timeout)
        else:
            if self.debug: print('self.prompt_expect timeout')
            raise pexpect.TIMEOUT('Timeout')

    def prompt(self, **kargs):
        if self.debug: print('Method self.prompt')
        try:
            self.prompt_expect(**kargs)
        except pexpect.TIMEOUT:
            if self.debug: print('self.prompt timeout')
            try:
                self.prompt_guess()
                self.connect.sendline()
                self.prompt_expect(**kargs)
            except:
                sys.stderr.write('Error trying to expect device prompt')

    def __del__(self):
        if self.debug: print('Method __del__')
        if self.connect.terminate():
            if self.debug: print('Session ended')
