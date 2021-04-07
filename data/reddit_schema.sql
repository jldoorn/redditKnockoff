PRAGMA foreign_keys = ON;
CREATE TABLE User (
	user_id INTEGER PRIMARY KEY,
	handle TEXT NOT NULL,
	hash INT NOT NULL,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	profile_path TEXT NOT NULL
);
CREATE TABLE Post (
	post_id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	content TEXT NOT NULL,
	time_stamp TEXT NOT NULL,
	post_user_id INTEGER,
	CONSTRAINT fk_post_user_id
	FOREIGN KEY (post_user_id)
	REFERENCES User(user_id)
);
CREATE TABLE Vote (
	vote_id INTEGER PRIMARY KEY,
        weight INTEGER NOT NULL,
	vote_user_id INTEGER,
        vote_post_id INTEGER,
	CONSTRAINT fk_vote_user_id
	FOREIGN KEY (vote_user_id)
	REFERENCES User(user_id),
	CONSTRAINT fk_vote_post_id
	FOREIGN KEY (vote_post_id)
	REFERENCES Post(post_id)
);
