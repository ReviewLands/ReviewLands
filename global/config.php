<?php
// global/config.php - loads settings
$SETTINGS = json_decode(file_get_contents(__DIR__ . '/settings.json'), true);
if (!is_array($SETTINGS)) $SETTINGS = [];
function s($k, $d = '') {
    global $SETTINGS; return isset($SETTINGS[$k]) ? $SETTINGS[$k] : $d;
}
?>
