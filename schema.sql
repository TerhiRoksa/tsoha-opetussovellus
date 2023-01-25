CREATE TABLE Users (
	id SERIAL PRIMARY KEY, 
	username TEXT UNIQUE, 
	password TEXT, 	
	usertype INTEGER);

