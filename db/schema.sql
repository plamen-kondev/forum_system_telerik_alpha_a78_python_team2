-- Run: mariadb -h 127.0.0.1 -u forum_user -pforum_pass < db/schema.sql
CREATE DATABASE IF NOT EXISTS hot_takes
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hot_takes;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS topic_members;
DROP TABLE IF EXISTS reply_votes;
DROP TABLE IF EXISTS replies;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;



CREATE TABLE users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    first_name    VARCHAR(32)  NOT NULL,
    last_name     VARCHAR(32)  NOT NULL,
    email         VARCHAR(255) NOT NULL UNIQUE,
    username      VARCHAR(16)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    is_blocked    BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_users_first_name CHECK (CHAR_LENGTH(first_name) BETWEEN 2 AND 32),
    CONSTRAINT chk_users_last_name  CHECK (CHAR_LENGTH(last_name)  BETWEEN 2 AND 32),
    CONSTRAINT chk_users_username   CHECK (CHAR_LENGTH(username)   BETWEEN 2 AND 16)
);


CREATE TABLE categories (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
);



CREATE TABLE topics (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    author_id     INT          NOT NULL,
    category_id   INT          NOT NULL,
    title         VARCHAR(128) NOT NULL,
    content       TEXT         NOT NULL,
    is_locked     BOOLEAN      NOT NULL DEFAULT FALSE,
    is_private    BOOLEAN      NOT NULL DEFAULT FALSE,
    best_reply_id INT          NULL,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_topics_title   CHECK (CHAR_LENGTH(title)   BETWEEN 16 AND 128),
    CONSTRAINT chk_topics_content CHECK (CHAR_LENGTH(content) BETWEEN 32 AND 8192),
    -- Deleting a user deletes their topics
    CONSTRAINT fk_topics_author   FOREIGN KEY (author_id)   REFERENCES users(id)      ON DELETE CASCADE,
    -- A category in use can't be deleted
    CONSTRAINT fk_topics_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);



CREATE TABLE replies (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    topic_id   INT      NOT NULL,
    author_id  INT      NOT NULL,
    content    TEXT     NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_replies_content CHECK (CHAR_LENGTH(content) BETWEEN 2 AND 8192),
    CONSTRAINT fk_replies_topic  FOREIGN KEY (topic_id)  REFERENCES topics(id) ON DELETE CASCADE,
    CONSTRAINT fk_replies_author FOREIGN KEY (author_id) REFERENCES users(id)  ON DELETE CASCADE
);


ALTER TABLE topics
    ADD CONSTRAINT fk_topics_best_reply
    FOREIGN KEY (best_reply_id) REFERENCES replies(id) ON DELETE SET NULL;



CREATE TABLE reply_votes (
    user_id  INT     NOT NULL,
    reply_id INT     NOT NULL,
    is_like  BOOLEAN NOT NULL,
    PRIMARY KEY (user_id, reply_id),
    CONSTRAINT fk_votes_user  FOREIGN KEY (user_id)  REFERENCES users(id)   ON DELETE CASCADE,
    CONSTRAINT fk_votes_reply FOREIGN KEY (reply_id) REFERENCES replies(id) ON DELETE CASCADE
);



CREATE TABLE topic_members (
    topic_id INT NOT NULL,
    user_id  INT NOT NULL,
    added_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (topic_id, user_id),
    CONSTRAINT fk_members_topic FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    CONSTRAINT fk_members_user  FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE
);