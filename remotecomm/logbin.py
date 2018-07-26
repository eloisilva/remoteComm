#! /usr/bin/env python3
#################################################################################
#     File Name           :     remotecomm/logbin.py
#     Created By          :     Eloi Silva (eloi@how2security.com.br)
#     Creation Date       :     [2017-07-13 16:26]
#     Last Modified       :     [2018-07-25 18:56]
#     Description         :      
#################################################################################


class logbin:
    def __init__(self):
        self.data = b''
    def write(self, d):
        self.data += d
    def flush(self):
        pass
    def tell(self):
        return len(tell)
    def __str__(self):
        return self.data.decode()
