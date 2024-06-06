<?php
// index.php

require_once('config.php');
require_once('router.php');

$router = new Router();

$router->post('/register', function() {
    require('register.php');
});

$router->post('/login', function() {
    require('login.php');
});

$router->get('/profile', function() {
    require('profile.php');
});

$router->run();
?>

