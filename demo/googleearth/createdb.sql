DROP TABLE IF EXISTS Description CASCADE;
DROP TABLE IF EXISTS Landmarks CASCADE;

CREATE TABLE Description
(
	  name character(300),
	  desc_id character(20) primary key,
	  address character(300),
	  date_built character(20),
	  architect character(300),
	  landmark date
)
WITH (
	  OIDS=TRUE
);

CREATE TABLE Landmarks
(
	  latitude numeric,
	  longitude numeric,
	  mark character (300),
	  color character(20),
	  scale real,
	  shortname character(300),
	  land_id character(20) primary key
)
WITH (
	  OIDS=TRUE
);
