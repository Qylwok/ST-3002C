CREATE TABLE IF NOT EXISTS Result(
     resultId INT UNSIGNED NOT NULL AUTO_INCREMENT, 
     competitionId VARCHAR(32) NOT NULL, 
     eventId VARCHAR(8) NOT NULL, 
     roundTypeId CHAR(1) NOT NULL, 
     best INT NOT NULL, 
     average INT NOT NULL, 
     personId VARCHAR(16) NOT NULL, 
     time1 INT NOT NULL, 
     time2 INT NOT NULL, 
     time3 INT NOT NULL, 
     time4 INT NOT NULL, 
     time5 INT NOT NULL, 
     recordSingleType VARCHAR(32), 
     recordAverageType VARCHAR(32),
     PRIMARY KEY (resultId)
);


CREATE TABLE IF NOT EXISTS Competition(
     competitionId VARCHAR(64) NOT NULL, 
     competitionName VARCHAR(256) NOT NULL, 
     cityId INT UNSIGNED NOT NULL, 
     dateBeginId INT UNSIGNED NOT NULL, 
     dateEndId INT UNSIGNED NOT NULL, 
     venue VARCHAR(256),
     PRIMARY KEY (competitionId)
);

CREATE TABLE IF NOT EXISTS Date_comp(
     dateId INT UNSIGNED NOT NULL AUTO_INCREMENT, 
     dateComp DATE NOT NULL,
     PRIMARY KEY (dateId)
);

CREATE TABLE IF NOT EXISTS City(
     cityId INT UNSIGNED NOT NULL AUTO_INCREMENT, 
     cityName VARCHAR(256) NOT NULL, 
     countryId VARCHAR(64) NOT NULL, 
     cityLongitude INT NOT NULL, 
     cityLatitude INT NOT NULL,
     PRIMARY KEY (cityId)
);


CREATE TABLE IF NOT EXISTS Country(
     countryId VARCHAR(64) NOT NULL, 
     countryName VARCHAR(64) NOT NULL, 
     continentId VARCHAR(32) NOT NULL, 
     iso2 VARCHAR(32) NOT NULL,
     PRIMARY KEY (countryId)
);

CREATE TABLE IF NOT EXISTS Continent(
     continentId VARCHAR(32) NOT NULL, 
     recordName VARCHAR(4) NOT NULL, 
     continentName VARCHAR(32) NOT NULL,
     PRIMARY KEY (continentId)
);

CREATE TABLE IF NOT EXISTS Person(
     personId VARCHAR(10) NOT NULL, 
     personName VARCHAR(128) NOT NULL, 
     countryId VARCHAR(64) NOT NULL, 
     gender CHAR(1) NOT NULL,
     PRIMARY KEY (personId)
);

CREATE TABLE IF NOT EXISTS Event(
     eventId VARCHAR(8) NOT NULL, 
     eventName VARCHAR(128) NOT NULL,
     PRIMARY KEY (eventId)
);

CREATE TABLE IF NOT EXISTS RoundType(
     roundTypeId CHAR(1) NOT NULL, 
     roundTypeName VARCHAR(32) NOT NULL,
     PRIMARY KEY (roundTypeId)
);


ALTER TABLE Result
     ADD FOREIGN KEY (competitionId) REFERENCES Competition(competitionId),
     ADD FOREIGN KEY (eventId) REFERENCES Event(eventId),
     ADD FOREIGN KEY (roundTypeId) REFERENCES RoundType(roundTypeId),
     ADD FOREIGN KEY (personId) REFERENCES Person(personId)
;

ALTER TABLE Competition
     ADD FOREIGN KEY (cityId) REFERENCES City(cityId),
     ADD FOREIGN KEY (dateBeginId) REFERENCES Date_comp(dateId),
     ADD FOREIGN KEY (dateEndId) REFERENCES Date_comp(dateId)
;

ALTER TABLE City
     ADD FOREIGN KEY (countryId) REFERENCES Country(countryId)
;

ALTER TABLE Country
     ADD FOREIGN KEY (continentId) REFERENCES Continent(continentId)
;

ALTER TABLE Person
     ADD FOREIGN KEY (countryId) REFERENCES Country(countryId)
;
