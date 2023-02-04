CREATE TABLE Users (
	id SERIAL PRIMARY KEY, 
	username TEXT UNIQUE, 
	password TEXT, 	
	usertype INTEGER
);

CREATE TABLE Courses (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE polls (
    id SERIAL PRIMARY KEY,
    topic TEXT
);

CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER REFERENCES polls,
    choice TEXT
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    choice_id INTEGER REFERENCES choices
);

CREATE TABLE material (
    id SERIAL PRIMARY KEY,
    content TEXT,
    course_id INTEGER REFERENCES courses
);
