=================
samsung_remote.py
=================

A Samsung TV Remote Control Python Script

Description
===========

samsung_remote is a script writen in Python that can remotely control your Samsung Smart TV thru wifi. It supports some nice features, such as:

- scan the network to find all available TV's;
- turn off all the found TV's with one command;
- specify which TV's to send commands;
- save common routines in a macro file to be executed latter. (video of a macro being executed: https://youtu.be/UXxBB7BOMDM)

Usage
=====

./samsung_remote.py [-h] [-s] [-k KEY] [-p] [-i IP] [-a] [-m MACRO]

  -h, --help              show this help message and exit
  -s, --scan              scans the TV on the network
  -k KEY, --key KEY       the key to be sent to TV
  -p, --poweroff          search all TV's in the network and turn them off
  -i IP, --ip IP          defines the ip of the TV that will receive the command
  -a, --auto              sends the command to the first TV available
  -m MACRO, --macro MACRO the macro file with commands to be sent to TV

Dependecies
===========

- Python 3.5
- `samsungctl <https://github.com/Ape/samsungctl>` (you can install it running # pip install samsungctl)

References
==========

- SSDP discovery https://gist.github.com/dankrause/6000248 and http://forum.micasaverde.com/index.php?topic=7878.15
- https://gist.github.com/danielfaust/998441
- 