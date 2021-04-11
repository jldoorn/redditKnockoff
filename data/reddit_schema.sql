PRAGMA foreign_keys = ON;
CREATE TABLE User (
	user_id INTEGER PRIMARY KEY,
	handle TEXT ,
	hash INT ,
	first_name TEXT ,
	last_name TEXT ,
	profile_path TEXT 
);
CREATE TABLE Post (
	post_id INTEGER PRIMARY KEY,
	title TEXT,
	content TEXT,
	time_stamp TEXT DEFAULT CURRENT_TIMESTAMP,
	post_user_id INTEGER,
	CONSTRAINT fk_post_user_id
	FOREIGN KEY (post_user_id)
	REFERENCES User(user_id)
);
CREATE TABLE Vote (
	vote_id INTEGER PRIMARY KEY,
        weight INTEGER ,
	vote_user_id INTEGER,
        vote_post_id INTEGER,
	CONSTRAINT fk_vote_user_id
	FOREIGN KEY (vote_user_id)
	REFERENCES User(user_id),
	CONSTRAINT fk_vote_post_id
	FOREIGN KEY (vote_post_id)
	REFERENCES Post(post_id)
);
