CREATE TABLE IF NOT EXISTS lms_user (
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    encrypted_password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    CONSTRAINT pk_lms_user PRIMARY KEY (user_id),
    CONSTRAINT un_username UNIQUE (username)
);
