#! /usr/bin/env python3
#################################################################################
#     File Name           :     test.py
#     Created By          :     Eloi Silva
#     Creation Date       :     [2018-07-27 16:50]
#     Last Modified       :     [2018-07-28 04:19]
#     Description         :      
#################################################################################

import getpass
import remotecomm
from remotecomm import command

jump = '200.204.1.12'
username = 'a0046772'
password = getpass.getpass()
timeout = 1.0

conn = command.remoteCMD(jump, username, password)
conn.jump()

def main():
    conn.prompt_guess()
