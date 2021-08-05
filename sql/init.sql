CREATE TABLE "People" (
    "Name" VARCHAR   NOT NULL,
    "Gender" VARCHAR   NOT NULL,
    "Homeworld" VARCHAR   NOT NULL,
    "Starships" VARCHAR   NOT NULL,
    CONSTRAINT "pk_People" PRIMARY KEY (
        "Name"
     )
);

CREATE TABLE "Starships" (
    "Name" VARCHAR   NOT NULL,
    "Model" VARCHAR   NOT NULL,
    "Manufacturer" VARCHAR   NOT NULL,
    "Lading" VARCHAR   NOT NULL,
    "Passengers" VARCHAR   NOT NULL,
    CONSTRAINT "pk_Starships" PRIMARY KEY (
        "Name"
     )
);

ALTER TABLE "People" ADD CONSTRAINT "fk_People_Starships" FOREIGN KEY("Starships")
REFERENCES "Starships" ("Name");
