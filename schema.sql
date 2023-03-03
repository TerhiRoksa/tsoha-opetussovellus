CREATE TABLE users (
	id SERIAL PRIMARY KEY, 
	username TEXT UNIQUE, 
	password TEXT, 	
	usertype INTEGER
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    visible BOOLEAN
);

CREATE TABLE polls (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    course_id INTEGER REFERENCES courses,
    answer TEXT
);

CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER REFERENCES polls,
    choice TEXT
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    choice_id INTEGER REFERENCES choices
    user_id INTEGER REFERENCES users
);

CREATE TABLE material (
    id SERIAL PRIMARY KEY,
    content TEXT,
    course_id INTEGER REFERENCES courses
);
