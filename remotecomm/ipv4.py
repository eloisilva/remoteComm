#! /usr/bin/env python3
#################################################################################
#     File Name           :     valida_ipv4.py
#     Created By          :     Eloi Silva
#     Creation Date       :     [2017-12-28 21:59]
#     Last Modified       :     [2017-12-28 22:26]
#     Description         :      
#################################################################################

def is_ipv4_octeto(n):
    n_bin = bin(int(n))[2:]
    if len(n_bin) < 1 or len(n_bin) > 8:
        return False
    else:
        return True

def ipv4_split(ip):
    if '/' in ip:
        return ip.rstrip().split('/')[0].split('.')
    else:
        return ip.rstrip().split('.')

def is_ipv4(ip):
    ip = ipv4_split(ip)
    if len(ip) == 4:
        for n in ip:
            if not is_ipv4_octeto(n):
                return False
        return '.'.join(ip)
    else:
        return False
