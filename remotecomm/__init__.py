#! /usr/bin/env python3
#################################################################################
#     File Name           :     remotecomm/__init__.py
#     Created By          :     Eloi Silva (eloi@how2security.com.br)
#     Creation Date       :     [2018-07-25 18:22]
#     Last Modified       :     [2018-09-01 00:42]
#     Description         :      
#################################################################################

import sys

__version__ = '1.0.3-dev1'
__author__ = 'Eloi Luiz da Silva'
__email__ = 'eloi@how2security.com.br'

if sys.version_info[0] < 3:
    msg = 'Python Version 3 required'
    raise ImportError(msg)
