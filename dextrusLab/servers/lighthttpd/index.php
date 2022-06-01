<?php
	$body =  file_get_contents( 'php://input' );
	echo "Body Length: " . strlen($body) . " Body: " . $body ;
?>