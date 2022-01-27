<p align="center"><img width=450 alt="PyShell" src="https://github.com/JoelGMSec/PyShell/blob/main/PyShell.png"></p>

# PyShell
**PyShell** is Multiplatform Python WebShell. This tool helps you to obtain a shell-like interface on a web server to be remotely accessed. Unlike other webshells, the main goal of the tool is to use as little code as possible on the server side, regardless of the language used or the operating system of the server.

Thanks to this, you can use different types of shells (aspx, php, jsp, sh, py...) both in Windows and Linux, with command history, upload and download files and even, moving through directories as if it were a standard shell.

# Requirements
- Python 3
- Install requirements.txt


# Download
It is recommended to clone the complete repository or download the zip file.
You can do this by running the following command:
```
git clone https://github.com/JoelGMSec/PyShell
```


# Usage
```
./PyShell.py -h


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

usage: pyshell.py [-h] [-a AUTH] [-c COOKIES] [-p PARAM] [-pi] [-su] [-ps] url method

positional arguments:
  url                   Webshell URL
  method                HTTP Method to execute command (GET or POST)

optional arguments:
  -h, --help            show this help message and exit
  -a AUTH, --auth AUTH  Authorization header to use on each request
  -c COOKIES, --cookies COOKIES
                        Cookie header to use on each request
  -p PARAM, --param PARAM
                        Parameter to use with custom WebShell
  -pi, --pipe           Pipe all commands after parameter
  -su, --sudo           Sudo command execution (Only on Linux hosts)
  -ps, --PowerShell     PowerShell command execution (Only on Windows hosts)
```

### The detailed guide of use can be found at the following link:

https://darkbyte.net/pyshell-multiplatform-python-webshell


# License
This project is licensed under the GNU 3.0 license - see the LICENSE file for more details.


# Credits and Acknowledgments
This tool has been created and designed from scratch by Joel Gámez Molina (@JoelGMSec) and Héctor de Armas Padrón (@3v4si0n)


# Contact
This software does not offer any kind of guarantee. Its use is exclusive for educational environments and / or security audits with the corresponding consent of the client. I am not responsible for its misuse or for any possible damage caused by it.

For more information, you can find us on Twitter as [@JoelGMSec](https://twitter.com/JoelGMSec),  [@3v4si0n](https://twitter.com/3v4si0n) and on my blog [darkbyte.net](https://darkbyte.net).


# Support
You can support my work buying me a coffee:

[<img width=250 alt="buymeacoffe" src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png">](https://www.buymeacoffee.com/joelgmsec)
