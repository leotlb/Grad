SET search_path TO "Grupo10";

CREATE TABLE CIRCUITS (
	CircuitID numeric(3) NOT NULL,
	CircuitRef varchar(30) NOT NULL,
	Name varchar(60),
	Location varchar(60),
	Country varchar(30),
	Lat numeric(7,4),
	Lng numeric(8,4),
	Alt numeric(4),
	URL text,
	CONSTRAINT CircuitPK PRIMARY KEY (CircuitID),
	CONSTRAINT CircuitSK UNIQUE (CircuitRef),
	CONSTRAINT CircuitLatCheck CHECK (Lat >= -90 AND Lat <= 90),
	CONSTRAINT CircuitLngCheck CHECK (Lng >= -180 AND Lng <= 180)
);


CREATE TABLE CONSTRUCTORS (
	ConstructorID numeric(4) NOT NULL,
	ConstructorRef varchar(30) NOT NULL,
	Name varchar(60),
	Nationality varchar(30),
	URL text,
	CONSTRAINT ConstructorsPK PRIMARY KEY (ConstructorID),
	CONSTRAINT ConstructorsSK UNIQUE (ConstructorRef)
);


CREATE TABLE DRIVER (
	DriverID numeric(4) NOT NULL,
	DriverRef varchar(30) NOT NULL,
	Number numeric(2),
	Code char(3),
	Forename varchar(30),
	Surname varchar(30),
	DateofBirth date,
	Nationality varchar(30),
	URL text,
	CONSTRAINT DriverPK PRIMARY KEY (DriverID),
	CONSTRAINT DriverSK UNIQUE (DriverRef)
);


CREATE TABLE SEASONS (
	Year numeric(4) NOT NULL,
	URL text,
	CONSTRAINT SeasonPK PRIMARY KEY (Year)
);


CREATE TABLE PITSTOPS (
	RaceID numeric(5) NOT NULL,
	DriverID numeric(4) NOT NULL
	Stop numeric(3) NOT NULL,
	Lap numeric(3) NOT NULL,
	Time time,
	Duration time,
	Milliseconds numeric(7),
	CONSTRAINT PitstopsPK PRIMARY KEY (RaceID, DriverID, Stop),
	CONSTRAINT Pitstops_Races_FK FOREIGN KEY (RaceID)
		REFERENCES RACES (RaceID)
			ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT Pitstops_Driver_FK FOREIGN KEY (DriverID)
		REFERENCES DRIVER (DriverID)
			ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE QUALIFYING (
	QualifyID numeric(5) NOT NULL,
	RaceID numeric(5),
	DriverID numeric(4),
	ConstructorID numeric(4),
	Time time,
	Number numeric(3),
	Postion numeric(3),
	Q1 varchar(10),
	Q2 varchar(10),
	Q3 varchar(10),
	CONSTRAINT QualifyingPK PRIMARY KEY (QualifyID),
	CONSTRAINT Qualifying_Races_FK FOREIGN KEY (RaceID)
		REFERENCES RACES (RaceID)
			ON UPDATE CASCADE ON DELETE SET NULL,
	CONSTRAINT Qualifying_Driver_FK FOREIGN KEY (DriverID)
		REFERENCES DRIVER (DriverID)
			ON UPDATE CASCADE ON DELETE SET NULL,
	CONSTRAINT Qualifying_Constructor_FK FOREIGN KEY (ConstructorID)
		REFERENCES CONSTRUCTORS (ConstructorID)
			ON UPDATE CASCADE ON DELETE SET NULL
);


CREATE TABLE STATUS (
	StatusID numeric(5) PRIMARY KEY,
	Status varchar(30)
);


CREATE TABLE RESULTS (
    ResultId numeric(5) PRIMARY KEY,
    RaceID numeric(5),
	DriverID numeric(4),
	ConstructorID numeric(4),
    Number numeric(3),
    Grid numeric(3),
    Postion numeric(3),
    PositionText varchar(3),
    PositionOrder numeric(3),
    Points numeric(3),
    Laps numeric(3),
    Time varchar(20),
    Milliseconds numeric(8),
    FastestLap numeric(3),
    Rank INTEGER,
    FastestLapTime time,
    FastestLapSpeed numeric(10),
    StatusID numeric(5) NOT NULL,
    CONSTRAINT Results_Races_FK FOREIGN KEY (RaceID)
        REFERENCES RACES (RaceID)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT Results_Drivers_FK FOREIGN KEY (DriverID)
        REFERENCES DRIVERS (DriverID)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT Results_Constructors_FK FOREIGN KEY (ConstructorID)
        REFERENCES CONSTRUCTORS (constructorId)
        ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT Results_Status_FK FOREIGN KEY (StatusID)
        REFERENCES STATUS (statusID)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE LAPTIMES (
	RaceID numeric(5) NOT NULL,
	DriverID numeric(4) NOT NULL
	Lap numeric(3) NOT NULL,
	Position numeric(2),
	Time time,
	Milliseconds numeric(7),
	CONSTRAINT LapTimesPK PRIMARY KEY (RaceID, DriverID, Lap),
	CONSTRAINT Laptimes_Races_FK FOREIGN KEY (RaceID)
		REFERENCES RACES (RaceID)
			ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT Laptimes_Driver_FK FOREIGN KEY (DriverID)
		REFERENCES DRIVER (DriverID)
			ON UPDATE CASCADE ON DELETE CASCADE
);

/* 	
Staging Table pra filtrar o lixo que vem de races.csv
	1.Importa o dados para a tabela RACESSTAGING
	2.Executa
		ALTER TABLE RACESSTAGING
			DROP COLUMN Trash1,
			DROP COLUMN Trash2,
			DROP COLUMN Trash3,
			DROP COLUMN Trash4,
			DROP COLUMN Trash5,
			DROP COLUMN Trash6,
			DROP COLUMN Trash7,
			DROP COLUMN Trash8,
			DROP COLUMN Trash9,
			DROP COLUMN Trash10;
	3.Executa
		INSERT INTO RACES
			SELECT * FROM RACESSTAGING;
	4.Executa
		DROP TABLE RACESSTAGING
*/
CREATE TABLE RACESSTAGING (
	RaceID numeric(5) NOT NULL PRIMARY KEY,
	Year numeric(4),
	Round numeric(2),
	CircuitID numeric(3),
	Name varchar(60),
	Date date,
	Time time,
	URL text,
	Trash1 date,
	Trash2 time,
	Trash3 date,
	Trash4 time,
	Trash5 date,
	Trash6 time,
	Trash7 date,
	Trash8 time,
	Trash9 date,
	Trash10 time
);


-- No caso de atualizacao de um temportada ou circuito faz sentido que as corridas associadas ao mesmo tambem sejam atualizadas
-- Todavia no caso de uma remocao de uma temporada ou circuito, caso a corrida ja tivesse acontecido faz sentido mante-la
-- na base visto que outras tabelas dependem da mesma e podem conter informacoes pertinentes
CREATE TABLE RACES (
	RaceID numeric(5) NOT NULL,
	Year numeric(4),
	Round numeric(2),
	CircuitID numeric(3),
	Name varchar(60),
	Date date,
	Time time,
	URL text,
	CONSTRAINT RacesPK PRIMARY KEY (RaceID),
	CONSTRAINT Season_of_RaceFK FOREIGN KEY (Year)
		REFERENCES SEASONS (Year)
			ON UPDATE CASCADE ON DELETE SET NULL,
	CONSTRAINT Circuit_of_RaceFK FOREIGN KEY (CircuitID)
		REFERENCES CIRCUITS (CircuitID)
			ON UPDATE CASCADE ON DELETE SET NULL
);


CREATE TABLE GEOCITIES15K (
	GeonameID integer NOT NULL,
	Name varchar(60),
	AsciiName varchar(60),
	AlternateNames text,
	Lat varchar(12),
	Long varchar(12),
	FeatureClass char(1),
	FeatureCode varchar(6),
	Country char(2),
	CC2 varchar(6),
	Admin1Code text,
	Admin2Code text,
	Admin3Code text,
	Admin4Code text,
	Population integer,
	Elevation varchar(5),
	Dem numeric(6),
	TimeZone varchar(60),
	Modification date,
	CONSTRAINT Geocities15KPK PRIMARY KEY (GeonameID)
);


CREATE TABLE COUNTRIES (
	ID numeric(7) NOT NULL,
	Code char(2) NOT NULL,
	Name varchar(60),
	Continent char(2),
	WikipediaLink text,
	Keywords text,
	CONSTRAINT CountriesPK PRIMARY KEY (ID),
	CONSTRAINT CountriesSK UNIQUE (code)
);


/* 	
Staging Table pra filtrar o lixo que vem de airports.csv
	1.Importa o dados para tabela AIRPORTSSTAGING
	2.Executa
		ALTER TABLE AIRPORTSSTAGING
			DROP COLUMN ICAOCode;
	3.Executa
		INSERT INTO AIRPORTS
			SELECT * FROM AIRPORTSSTAGING;
	4.Executa
		DROP TABLE AIRPORTSSTAGING
*/
CREATE TABLE AIRPORTSSTAGING (
	ID numeric(6) NOT NULL PRIMARY KEY,
	IDent varchar(8),
	Type varchar(30),
	Name text,
	LatDeg varchar(30),
	LongDeg varchar(30),
	ElevFt numeric(6),
	Continent char(2),
	ISOCountry char(2),
	ISORegion varchar(8),
	City varchar(100),
	Scheduled_service varchar(3),
	ICAOCode varchar(4),
	IATACode varchar(4),
	GPSCode varchar(9),
	LocalCode varchar(9),
	HomeLink text,
	WikipediaLink text,
	Keywords text
);


CREATE TABLE AIRPORTS (
	ID numeric(6) NOT NULL,
	IDent varchar(8) NOT NULL,
	Type varchar(30),
	Name text,
	LatDeg varchar(30),
	LongDeg varchar(30),
	ElevFt numeric(6),
	Continent char(2),
	ISOCountry char(2),
	ISORegion varchar(8),
	City varchar(100),
	Scheduled_service varchar(3),
	IATACode varchar(4),
	GPSCode varchar(9),
	LocalCode varchar(9),
	HomeLink text,
	WikipediaLink text,
	Keywords text,
	CONSTRAINT AirportsPK PRIMARY KEY (ID),
	CONSTRAINT AirportsSK UNIQUE (IDent)
);


-- Se a corrida referenciada pelo resultado for deletada ou alterada faz sentido que o mesmo aconteceria ao resultado
-- Se o corredor for alterado a associação ao resultado também deverá ser alterada
-- Todavia não faz sentido remover um corredor que participou de corridas e possui resultados, assim cabe a quem administra
-- a base de tratar do resultados individualmente primeiro
CREATE TABLE DRIVERSTANDINGS (
	DriverStandingID numeric(7) NOT NULL,
	RaceID numeric(5) NOT NULL,
	DriverID numeric(4) NOT NULL,
	Points float,
	Position varchar(3),
	PositionText varchar(3),
	Wins integer,
	CONSTRAINT DriverStandingsPK PRIMARY KEY (DriverStandingID),
	CONSTRAINT Race_of_DriverStandingFK FOREIGN KEY (RaceID)
		REFERENCES RACES (RaceID)
			ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT Driver_of_DriverStandingFK FOREIGN KEY (DriverID)
		REFERENCES DRIVER (DriverID)
			ON UPDATE CASCADE ON DELETE RESTRICT
);