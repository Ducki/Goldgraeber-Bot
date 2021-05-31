-- -------------------------------------------------------------
-- TablePlus 3.12.8(368)
--
-- https://tableplus.com/
--
-- Database: text.sqlite
-- Generation Time: 2021-05-31 22:32:21.8650
-- -------------------------------------------------------------

CREATE TABLE Triggers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	searchstring VARCHAR
);

CREATE TABLE Answers (
	id integer primary key autoincrement,
	trigger_id integer,
	answer varchar,
	foreign key (trigger_id) REFERENCES Triggers(id)

);
