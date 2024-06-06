<?php
// login.php

require_once('config.php');

// เชื่อมต่อฐานข้อมูล MySQL
$conn = mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME);

// ตรวจสอบการเชื่อมต่อ
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// รับข้อมูลจากฟอร์ม
$username = $_POST['username'];
$password = $_POST['password'];

// ดึงข้อมูลผู้ใช้จากฐานข้อมูล
$sql = "SELECT * FROM users WHERE username='$username'";
$result = mysqli_query($conn, $sql);

if (mysqli_num_rows($result) > 0) {
    $row = mysqli_fetch_assoc($result);
    if (password_verify($password, $row['password'])) {
        echo json_encode(['message' => 'ล็อกอินสำเร็จ']);
    } else {
        echo json_encode(['error' => 'รหัสผ่านไม่ถูกต้อง']);
    }
} else {
    echo json_encode(['error' => 'ไม่พบผู้ใช้']);
}

mysqli_close($conn);
?>
