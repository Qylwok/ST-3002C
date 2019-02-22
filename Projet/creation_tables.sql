CREATE TABLE Result(         UNSIGNED INT resultId NOT NULL AUTO_INCREMENT, 
VARCHAR(32) competitionId NOT NULL, 
VARCHAR(8) eventId NOT NULL, 
CHAR(1) roundTypeId NOT NULL, 
INT best NOT NULL, 
INT average NOT NULL, 
VARCHAR(16)personId NOT NULL, 
INT value1 NOT NULL, 
INT value2 NOT NULL, 
INT value3 NOT NULL, 
INT value4 NOT NULL, 
INT value5 NOT NULL, 
VARCHAR(32) recordSingleType, 
VARCHAR(32) recordAverageType
                    PRIMARY KEY resultId,
                    FOREIGN KEY competitionId REFERENCES Competition(competitionId),
                    FOREIGN KEY eventId REFERENCES Event(eventId),
                    FOREIGN KEY roundTypeId REFERENCES RoundType(roundTypeId),
                    FOREIGN KEY personId REFERENCES Person(personId));

CREATE TABLE Competition(    VARCHAR(64) competitionId NOT NULL, 
VARCHAR(256) competitionName NOT NULL, 
UNSIGNED INT cityId NOT NULL AUTO_INCREMENT, 
DATE dateBeginId NOT NULL, 
DATE dateEndId NOT NULL, 
VARCHAR(256) venue,
                    PRIMARY KEY competitionId,
                    FOREIGN KEY cityId REFERENCES City(cityId),
                    FOREIGN KEY dateBeginId REFERENCES Date(dateId),
                    FOREIGN KEY dateEndId REFERENCES Date(dateId));

CREATE TABLE Date(           UNSIGNED INT dateId NOT NULL AUTO_INCREMENT, 
DATE date NOT NULL,
                    PRIMARY KEY dateId);

CREATE TABLE City(           UNSIGNED INT cityId NOT NULL AUTO_INCREMENT, 
VARCHAR(256) cityName NOT NULL, 
VARCHAR(64) countryId NOT NULL, 
INT cityLongitude NOT NULL, 
INT cityLatitude NOT NULL,
                    PRIMARY KEY cityId,
                    FOREIGN KEY countryId REFERENCES Country(countryId));


CREATE TABLE Country(        VARCHAR(64) countryId NOT NULL, 
VARCHAR(64) countryName NOT NULL, 
VARCHAR(32) continentId NOT NULL, 
VARCHAR(32) iso2 NOT NULL,
                    PRIMARY KEY countryId,
                    FOREIGN KEY continentId REFERENCES Continent(continentId));

CREATE TABLE Continent(      VARCHAR(32) continentId NOT NULL, 
VARCHAR(4) recordName NOT NULL, 
VARCHAR(32) continentName NOT NULL,
                    PRIMARY KEY continentId);

CREATE TABLE Championship(   UNSIGNED INT championshipId NOT NULL AUTO_INCREMENT, 
VARCHAR(64) competitionId NOT NULL, 
VARCHAR(32) championshipType,
                    PRIMARY KEY championshipId,
                    FOREIGN KEY competitionId REFERENCES Competition(competitionId));

CREATE TABLE Person(        VARCHAR(10) personId NOT NULL, 
VARCHAR(64) personName NOT NULL, 
VARCHAR(64) personSurname NOT NULL, 
VARCHAR(64) countryId NOT NULL, 
CHAR(1) gender NOT NULL,
                    PRIMARY KEY personId,
                    FOREIGN KEY countryId REFERENCES Country(countryId));

CREATE TABLE Event(         VARCHAR(8) eventId NOT NULL, 
VARCHAR(128) eventName NOT NULL,
                    PRIMARY KEY eventId);

CREATE TABLE RoundType(      CHAR(1) roundTypeId NOT NULL, 
VARCHAR(32) roundTypeName NOT NULL,
                    PRIMARY KEY roundTypeId);
