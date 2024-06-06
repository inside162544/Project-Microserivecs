<?php
// router.php

class Router {
    private $routes = [];

    public function post($url, $callback) {
        $this->routes['POST'][$url] = $callback;
    }

    public function get($url, $callback) {
        $this->routes['GET'][$url] = $callback;
    }

    public function run() {
        $method = $_SERVER['REQUEST_METHOD'];
        $url = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

        if (isset($this->routes[$method][$url])) {
            $callback = $this->routes[$method][$url];
            call_user_func($callback);
        } else {
            http_response_code(404);
            echo '404 Not Found';
        }
    }
}
?>
