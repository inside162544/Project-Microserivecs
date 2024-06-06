<?php
// register.php

require_once('config.php');

// เชื่อมต่อฐานข้อมูล MySQL
$conn = mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME);

// ตรวจสอบการเชื่อมต่อ
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// รับข้อมูลจากฟอร์ม
$username = $_POST['username'];
$email = $_POST['email'];
$password = password_hash($_POST['password'], PASSWORD_DEFAULT);

// แทรกข้อมูลผู้ใช้ลงในฐานข้อมูล
$sql = "INSERT INTO users (username, email, password) VALUES ('$username', '$email', '$password')";
if (mysqli_query($conn, $sql)) {
    echo json_encode(['message' => 'ลงทะเบียนผู้ใช้เรียบร้อย']);
} else {
    echo json_encode(['error' => 'การลงทะเบียนล้มเหลว']);
}

mysqli_close($conn);
?>
