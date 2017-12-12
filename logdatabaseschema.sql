#Schema to create logdatabase
CREATE TABLE logdatabase_google(
	logtime VARCHAR(19),
	pid INTEGER,
	tid INTEGER,
	log_tag VARCHAR(20),
	hash INTEGER,
	b_a VARCHAR(6),
	uid INTEGER,
	hook_type VARCHAR(10),
	associated_activity VARCHAR(100),
	class_name VARCHAR(50),
	method_name VARCHAR(50),
	arguments VARCHAR(500),
	return_value VARCHAR(500)
);



