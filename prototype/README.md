### This is be boiler plate for admin/auth for future app. Moving away from sqlalchemy sticking with raw sql.

### manually build the sql database

sqlite3 users.db
CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0
);
.exit

### add admin to database
sqlite3 users.db
INSERT INTO users (username, password, is_admin) VALUES ('admin', 'hash_is_generated_by_and_app', 1);

