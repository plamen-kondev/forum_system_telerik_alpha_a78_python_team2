-- Run once as an admin user: mariadb < db/setup_user.sql  (or: sudo mariadb < db/setup_user.sql)
CREATE DATABASE IF NOT EXISTS hot_takes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'forum_user'@'localhost' IDENTIFIED BY 'forum_pass';
CREATE USER IF NOT EXISTS 'forum_user'@'127.0.0.1' IDENTIFIED BY 'forum_pass';
GRANT ALL PRIVILEGES ON hot_takes.* TO 'forum_user'@'localhost';
GRANT ALL PRIVILEGES ON hot_takes.* TO 'forum_user'@'127.0.0.1';
FLUSH PRIVILEGES;