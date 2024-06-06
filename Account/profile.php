<?php
// profile.php

require_once('config.php');

session_start();

if (isset($_SESSION['username'])) {
    echo json_encode(['username' => $_SESSION['username']]);
} else {
    echo json_encode(['error' => 'ไม่ได้รับอนุญาต']);
}
?>
