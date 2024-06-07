<?php
session_start();
if(!isset($_POST['login'])){
        header("location:index.php");
        die();
}
$login = $_POST['login'];
$passwd = sha1($_POST['pwd']);
$name = $_POST['namelastname'];
$gender = $_POST['gender'];
$email = $_POST['email'];
include 'db.php';
$conn = new mysqli($host, $user, $pass, $db);
$sql = "SELECT * FROM user where username='$login'";
$result = $conn->query($sql);

if ($result->num_rows == 1) {
    $_SESSION['add_login'] = "error";
} else {
    $sql1 = "INSERT INTO user (username,password,fullname,gender,email,phoneNumber,role) 
        VALUES('$login','$passwd','$name','$gender','$email','phoneNumber','m')";
    $conn->query($sql1);

    if ($conn->affected_rows > 0) {
        $_SESSION['add_login'] = "success";
    } else {
        $_SESSION['add_login'] = "error";
    }
}

$conn->close();
header("location:register.php");
die();

?>