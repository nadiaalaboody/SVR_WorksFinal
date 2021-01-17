BEGIN TRANSACTION;
DROP TABLE IF EXISTS "companies";
CREATE TABLE IF NOT EXISTS "companies" (
	"companyid"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"phone"	NUMERIC NOT NULL,
	"contactname"	TEXT NOT NULL,
	"contactphone"	NUMERIC NOT NULL,
	"contactemail"	TEXT NOT NULL,
	"speciality"	TEXT NOT NULL,
	PRIMARY KEY("companyid")
);
DROP TABLE IF EXISTS "subscription";
CREATE TABLE IF NOT EXISTS "subscription" (
	"userid"	INTEGER NOT NULL,
	"opid"	INTEGER NOT NULL,
	FOREIGN KEY("userid") REFERENCES "users",
	FOREIGN KEY("opid") REFERENCES "opportunities"
);
DROP TABLE IF EXISTS "users";
CREATE TABLE IF NOT EXISTS "users" (
	"userid"	INTEGER NOT NULL UNIQUE,
	"usename"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"confirm"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("userid")
);
DROP TABLE IF EXISTS "opportunities";
CREATE TABLE IF NOT EXISTS "opportunities" (
	"opid"	INTEGER NOT NULL UNIQUE,
	"opname"	TEXT NOT NULL,
	"opcategory"	TEXT NOT NULL,
	"daterequired"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"skillsgained"	TEXT NOT NULL,
	"img_path"	TEXT,
	"companyid"	INTEGER,
	FOREIGN KEY("companyid") REFERENCES "companies",
	PRIMARY KEY("opid")
);
INSERT INTO "users" VALUES (1,'nadia1','Nadia','nadia@example.com','nadia@example.com','123');
INSERT INTO "users" VALUES (2,'muhsin1','muhsin','muhsin@example.com','muhsin@example.com','123');
INSERT INTO "users" VALUES (3,'sara1','Sara','sara@example.com','12','$5$rounds=535000$EazT/26BGf3Gcifn$tF26HefZz3vIG0EZoyXCdK7MCMdcA2Z8g.7b2MY1ap5');
INSERT INTO "users" VALUES (4,'ali12','Ali','ali@example.com','12','$5$rounds=535000$bPFP7tu0LUZd3otH$cwsC1OzZg0i7lwzFS7EQJ7trAAaXHb06Ugte8FlIGL5');
INSERT INTO "users" VALUES (5,'sam3','sam','sam@gmail.com','12','$5$rounds=535000$ThNI22S4Ke21DI7J$aEDmpc.agdjZCplLF1QKKaId6zDil6tARZAnUXqcs64');
INSERT INTO "users" VALUES (6,'nadia1','name','nadia@example.com','12','$5$rounds=535000$tHmWotxYbUh21Ldp$KNIpIuo9cZRtarliN0oRfhpAPK4556MazmO5wDlnL59');
INSERT INTO "users" VALUES (7,'nan2','nan','nan@example.com','12','$5$rounds=535000$I3oPBNOAIZNXpVZa$ZMz8zITnY7dW9Ll6G1YWQtiYGIk94z89knIU27vd.R3');
COMMIT;
