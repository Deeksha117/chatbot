<?php
//session_start();
//if(isset($_SESSION['name'])){
//echo "TRIPPO";
    $text = $_POST['text'];

    $host = "127.0.0.1";
    $port = 9988;

    // No Timeout 
    set_time_limit(0);
    $socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
    $result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");

    socket_write($socket, $text, strlen($text)) or die("Could not send data to server\n");
    $result = socket_read ($socket, 1024) or die("Could not read server response\n");
    echo "Reply From Server  :".$result;
    socket_close($socket);

    #$command = "python abc.py ".$text;
	#$output = shell_exec($command);
    $fp = fopen("log.html","a") or die("file not opened");
    //fwrite($fp, "<div class='msgln'>(".date("g:i A").") <b>".$_SESSION['name']."</b>: ".stripslashes(htmlspecialchars($text))."<br></div>");
    
    fwrite($fp, "<div class='msgln'>(".date("g:i A").") USER : ".stripslashes(htmlspecialchars($text))."<br>");
    fwrite($fp,"<div class='msgln' style='text-align: right;color: blue;'>(".date("g:i A").") TRIPPO : ".$result." </div>");
    //fwrite("hola trippo </div>");
    fclose($fp);
    echo "TRIPPO";
//}
?>