8<?php
session_start();

if (isset($_SESSION["username"]) && $_SESSION["id"] == session_id()) {
    header("location: index.php");
    die();
}

$u = $_POST['login'];
$p = $_POST['pwd'];
include 'db.php';

// Use prepared statement to prevent SQL injection
$sql = "SELECT * FROM user where username=? and password=SHA1(?)";
$stmt = $conn->prepare($sql);

if ($stmt === false) {
    die('Error in preparing the SQL statement.');
}

$stmt->bind_param("ss", $u, $p); // Assuming the password is stored as plaintext

$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows == 1) {
    $data = $result->fetch_assoc();
    
    // Set Session variables
    $_SESSION["username"] = $data["username"];
    $_SESSION["role"] = $data["role"];
    $_SESSION["user_id"] = $data["id"];
    $_SESSION["id"] = session_id();

    header("Location: index.php");
    die();
} else {
    $_SESSION["error"] = 1;
    header("Location: login.php");
    die();
}

$stmt->close();
$conn->close();
?>