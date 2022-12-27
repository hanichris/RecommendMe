-- Delete the following tables if present in the database.
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS professional;
DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS industry;

-- Implement `enum` datatype
CREATE TABLE IF NOT EXISTS userType (
    u_type TEXT PRIMARY KEY,
    seq INTEGER
);
INSERT OR REPLACE INTO userType(u_type, seq) VALUES('P', 1);
INSERT OR REPLACE INTO userType(u_type, seq) VALUES('S', 2);

-- Create the `user` table
CREATE TABLE IF NOT EXISTS user (
    user_id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    passwd TEXT NOT NULL,
    birthday TEXT NOT NULL,
    user_type TEXT NOT NULL REFERENCES userType(u_type)
);

-- Create the `post` table
CREATE TABLE IF NOT EXISTS post (
    post_id TEXT NOT NULL,
    author_id TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    body TEXT CHECK (LENGTH(body) <= 280) NOT NULL,
    PRIMARY KEY (post_id, author_id),
    FOREIGN KEY (author_id) REFERENCES user (user_id)
);

-- Create the `student` table
CREATE TABLE IF NOT EXISTS student (
    student_id TEXT PRIMARY KEY,
    field_of_study TEXT NOT NULL,
    degree TEXT NOT NULL,
    graduation INTEGER NOT NULL,
    school TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES user (user_id)
);

-- Create the `professional` table
CREATE TABLE IF NOT EXISTS professional (
    prof_id TEXT PRIMARY KEY,
    job_title TEXT NOT NULL,
    comp_id TEXT NOT NULL,
    FOREIGN KEY (prof_id) REFERENCES user (user_id),
    FOREIGN KEY (comp_id) REFERENCES company (company_id)
);

-- Create the `company` table
CREATE TABLE IF NOT EXISTS company (
    company_id TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    employee_id TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES user (user_id)
);