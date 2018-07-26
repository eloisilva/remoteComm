# remotecomm
Python module to access remote ssh servers using jumpserver

Important: This module is in development and has some issues, any help, bug report and code are welcome.

# Version 1.0.0-dev1
This version of remotecomm can be installed as a package using pip.

# Require
  * Python3
  * pexpect
  * ptyprocess

# Install
python3 setup.py install

-Or-

pip install remotecomm.tar.bz2

# Configure
Output remotecomm:
  Edit the python file /usr/local/lib/python3.5/dist-packages/remotecomm/__main__.py and change the debug and debug_dir variable to send the commands output to a file or stdout

Binary:
-remotecomm
  Edit the python file /usr/local/lib/python3.5/dist-packages/remotecomm/__main__.py and change the jump variable

-remoteexec
  Edit the python file /usr/local/lib/python3.5/dist-packages/remotecomm/jumpRemote.py and change the jump variable

# Usage
Importante:
  * Use hostname insted ip address.

Example remotecomm:
remotecomm router1 router2 router3 router4

Example remoteexec:
remoteexec
