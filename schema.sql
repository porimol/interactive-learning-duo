-- users definition
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT, 
    last_name TEXT, 
    email TEXT, 
    password TEXT, 
    photo BLOB
);

-- user_address definition
CREATE TABLE user_address (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    user_id INTEGER, 
    apartment TEXT, 
    building TEXT, 
    post_code_id INTEGER REFERENCES post_code (id) ON DELETE CASCADE ON UPDATE CASCADE, 
    city_id INTEGER REFERENCES city (id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL, 
    country_id REFERENCES country (id) ON DELETE CASCADE ON UPDATE CASCADE, 
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- city definition
CREATE TABLE city (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    city_name VARCHAR (255), 
    country_id INTEGER REFERENCES country (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- country definition
CREATE TABLE country (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    country_name VARCHAR (255)
);

-- post_code definition
CREATE TABLE post_code (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    code TEXT, 
    city_id INTEGER REFERENCES city (id) ON DELETE CASCADE ON UPDATE CASCADE, 
    country_id INTEGER REFERENCES country (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- question_category definition
CREATE TABLE question_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    category_name TEXT (6) UNIQUE
);

-- questions_answers definition
CREATE TABLE questions_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
    user_id INTEGER CONSTRAINT user_id REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE, 
    question TEXT, 
    answer TEXT, 
    question_category_id INTEGER REFERENCES question_category (id) ON DELETE CASCADE ON UPDATE CASCADE, 
    created_at TEXT
);

-- log definition
CREATE TABLE log (
	"" INTEGER PRIMARY KEY AUTOINCREMENT,
	question_answer_id INTEGER,
	user_id INTEGER,
	question_category_id INTEGER,
	question TEXT,
	answer TEXT,
	log_timestamp DATETIME
);
CREATE TRIGGER LogTrigger after delete on questions_answers 
BEGIN
    insert into log values(old.id, old.id, old.user_id, old.question_category_id, old.question, old.answer, DATETIME('NOW'));
END;
