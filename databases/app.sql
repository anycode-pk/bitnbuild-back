BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "polish_kings" (
	"id"			INTEGER NOT NULL,
	"name"			TEXT NOT NULL,
	"birth"			TEXT NOT NULL,
	"death"			TEXT NOT NULL,
	"reign_start"	TEXT NOT NULL,
	"image" 		BLOB NOT NULL,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "polish_kings_questions" (
	"id"				INTEGER NOT NULL,
	"question"			TEXT NOT NULL,
	"answers"			TEXT NOT NULL,
	"correct_answer"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;