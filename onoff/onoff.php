<?php
system("python onoff.py");
$file_name = "state.txt";
$state = file_get_contents($file_name);
$fp = fopen($file_name, 'w');
if($state == 1){
fwrite($fp, '0');
}else{
fwrite($fp, '1');
}
fclose($fp);
header("Location: index.php"); // Return to frontend (onoff.html)
?>