-- Create a MySQL database
CREATE DATABASE IF NOT EXISTS account_db;

-- Use the database
USE account_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Insert sample data (optional)
INSERT INTO users (username, email, password) VALUES 
('john_doe', 'john@example.com', 'password123'),
('jane_doe', 'jane@example.com', 'securepassword');
