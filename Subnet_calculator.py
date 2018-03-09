#!/usr/local/bin/python3.6

'''
This script uses the 'lsof' utility in Unix/ Linux to list the running process as per the port number specified by the user and kills the service if any!

Usage - ./KillPort 5500 
Given that the KillPort file has the excutable rights! To do so, use command chmod +x KillPort

'''

from argparse import ArgumentParser
import os
import subprocess

parser = ArgumentParser(description='Take input as port number and kill listening ports!!')
parser.add_argument('port', type=int, help='Enter the port number followed by the -p flag')

port = parser.parse_args().port

try:
    result = subprocess.run(
        ['lsof', '-n', "-i4TCP:%s" %port],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

except subprocess.CalledProcessError:
    print(f"No process listening on port: {port}")


# Let this be a pointer kind of var, to target the line that has a LISTEN in it
listening = None

for line in result.stdout.splitlines():
    if "LISTEN" in str(line):
        listening = line
        break

if listening:
    # Get the PID from the output
    pid = int(listening.split()[1])
    os.kill(pid, 9)
    print(f"PID {pid} killed..!!")

else:
    print(f"No process listening on the port {port}")

