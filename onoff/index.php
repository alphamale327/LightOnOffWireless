<?php
$state = file_get_contents('state.txt');
if($state == 1){
header("Location: on.html");
}else{
header("Location: off.html");
}

?>