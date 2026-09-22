<?php
// Auto-load the correct *-index.php file inside this tool folder
$files = glob(__DIR__ . "/*-index.php");

if (!$files) {
  http_response_code(404);
  echo "Tool entry file not found.";
  exit;
}

include $files[0];
