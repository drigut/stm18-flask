DROP TABLE IF EXISTS PEOPLE;

CREATE TABLE PEOPLE (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    GENDER TEXT NOT NULL,
    HOMEWORLD TEXT NOT NULL
);