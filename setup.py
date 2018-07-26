#! /usr/bin/env python3
#################################################################################
#     File Name           :     setup.py
#     Created By          :     Eloi Silva
#     Creation Date       :     [2018-07-25 18:10]
#     Last Modified       :     [2018-07-25 19:35]
#     Description         :      
#################################################################################

from setuptools import setup
import remotecomm

setup(
    name = 'remotecomm',
    version = remotecomm.__version__,
    author = remotecomm.__author__,
    author_email = remotecomm.__email__,
    packages = ['remotecomm',],
    license = 'GNU Version 3',
    entry_points={
        'console_scripts': [
            'remotecomm = remotecomm.__main__:main',
            'remoteexec = remotecomm.jumpRemote:main',
        ],
    },
    install_requires=[
        "pexpect",
        "ptyprocess",
        ],
)
