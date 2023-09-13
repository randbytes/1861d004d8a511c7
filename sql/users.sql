CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
	authorId TEXT NOT NULL,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	first_name_last_name TEXT NOT NULL,
	surname TEXT,
	position TEXT NOT NULL,
	project TEXT NOT NULL,
  avatar TEXT
);
