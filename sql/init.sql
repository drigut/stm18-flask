CREATE TABLE "People" (
    "CharacterID" int   NOT NULL,
    "Name" varchar   NOT NULL,
    "Gender" string   NOT NULL,
    "PlanetID" int   NOT NULL,
    "StarshipID" int   NOT NULL,
    CONSTRAINT "pk_People" PRIMARY KEY (
        "CharacterID"
     )
);

CREATE TABLE "Planets" (
    "PlanetID" int   NOT NULL,
    "Name" varchar   NOT NULL,
    CONSTRAINT "pk_Planets" PRIMARY KEY (
        "PlanetID"
     ),
    CONSTRAINT "uc_Planets_Name" UNIQUE (
        "Name"
    )
);

CREATE TABLE "Starships" (
    "StarshipID" int   NOT NULL,
    "Name" varchar   NOT NULL,
    "Model" varchar   NOT NULL,
    "ManufacturerID" int   NOT NULL,
    "Lading" string   NOT NULL,
    CONSTRAINT "pk_Starships" PRIMARY KEY (
        "StarshipID"
     ),
    CONSTRAINT "uc_Starships_Name" UNIQUE (
        "Name"
    ),
    CONSTRAINT "uc_Starships_Model" UNIQUE (
        "Model"
    )
);

CREATE TABLE "Manufacturer" (
    "ManufacturerID" int   NOT NULL,
    "Name" varchar   NOT NULL,
    CONSTRAINT "pk_Manufacturer" PRIMARY KEY (
        "ManufacturerID"
     ),
    CONSTRAINT "uc_Manufacturer_Name" UNIQUE (
        "Name"
    )
);

ALTER TABLE "People" ADD CONSTRAINT "fk_People_PlanetID" FOREIGN KEY("PlanetID")
REFERENCES "Planets" ("PlanetID");

ALTER TABLE "People" ADD CONSTRAINT "fk_People_StarshipID" FOREIGN KEY("StarshipID")
REFERENCES "Starships" ("StarshipID");

ALTER TABLE "Starships" ADD CONSTRAINT "fk_Starships_ManufacturerID" FOREIGN KEY("ManufacturerID")
REFERENCES "Manufacturer" ("ManufacturerID");

CREATE INDEX "idx_People_Name"
ON "People" ("Name");

