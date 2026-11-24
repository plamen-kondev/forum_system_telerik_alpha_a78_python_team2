-- Run after schema.sql:
-- mariadb -h 127.0.0.1 -u forum_user -pforum_pass < db/seed.sql
USE hot_takes;

INSERT INTO categories (name) VALUES
    ('Food'),
    ('Cars'),
    ('Travel'),
    ('Gaming'),
    ('Music'),
    ('Tech');

-- Users topics and replies will be added once registration (password hashing) is ready