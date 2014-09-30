/*

ComicVineDB schema

Database to house Comic Vine information

Created by Brian Cherinka   

*/

CREATE SCHEMA comicvinedb;

ALTER SCHEMA comicvinedb OWNER TO cvadmin;

SET search_path TO comicvinedb;

CREATE TABLE comicvinedb.character (pk SERIAL PRIMARY KEY NOT NULL, aliases TEXT, 
	issue_count INTEGER, deck TEXT, description TEXT, id INTEGER, name TEXT, 
	number_align_changes INTEGER, origin_pk INTEGER, alignment_pk INTEGER,
	enemies INTEGER[], friends INTEGER[], first_issue INTEGER, issues_died_in INTEGER[],
	team_friends INTEGER[], team_enemies INTEGER[]);

CREATE TABLE comicvinedb.origin (pk SERIAL PRIMARY KEY NOT NULL, id INTEGER, name TEXT);

CREATE TABLE comicvinedb.alignment (pk SERIAL PRIMARY KEY NOT NULL, label TEXT);

CREATE TABLE comicvinedb.character_to_team (pk SERIAL PRIMARY KEY NOT NULL, 
		character_pk INTEGER, team_pk INTEGER);

CREATE TABLE comicvinedb.character_to_power (pk SERIAL PRIMARY KEY NOT NULL, 
		character_pk INTEGER, power_pk INTEGER);

CREATE TABLE comicvinedb.character_to_creator (pk SERIAL PRIMARY KEY NOT NULL, 
		character_pk INTEGER, creator_pk INTEGER);
		
CREATE TABLE comicvinedb.character_to_identity (pk SERIAL PRIMARY KEY NOT NULL, 
		character_pk INTEGER, identity_pk INTEGER);

CREATE TABLE comicvinedb.character_to_issue (pk SERIAL PRIMARY KEY NOT NULL, 
		character_pk INTEGER, issue_pk INTEGER);

CREATE TABLE comicvinedb.creator (pk SERIAL PRIMARY KEY NOT NULL, aliases TEXT,
		birth TIMESTAMP, country TEXT, death TIMESTAMP, gender_pk INTEGER, hometown TEXT, id INTEGER, name TEXT,
		deck TEXT, description TEXT);

CREATE TABLE comicvinedb.creator_to_issue (pk SERIAL PRIMARY KEY NOT NULL, 
		creator_pk INTEGER, issue_pk INTEGER);
		
CREATE TABLE comicvinedb.identity (pk SERIAL PRIMARY KEY NOT NULL, birth TIMESTAMP,
	name TEXT, age INTEGER, gender_pk INTEGER, ethnicity_pk INTEGER, orientation_pk INTEGER);

CREATE TABLE comicvinedb.identity_to_species (pk SERIAL PRIMARY KEY NOT NULL, 
		identity_pk INTEGER, species_pk INTEGER);
						
CREATE TABLE comicvinedb.issue (pk SERIAL PRIMARY KEY NOT NULL, aliases TEXT,
	cover_date TIMESTAMP, deck TEXT, description TEXT, id INTEGER, issue_number INTEGER,
	name TEXT, store_date TIMESTAMP, volume_pk INTEGER, characters_died INTEGER[], 
	teams_disbanded INTEGER[], first_appearances INTEGER[], first_appearance_teams INTEGER[],
	first_appearance_locations INTEGER[]);
							
CREATE TABLE comicvinedb.team (pk SERIAL PRIMARY KEY NOT NULL, aliases TEXT, 
	issue_count INTEGER, member_count INTEGER, deck TEXT, description TEXT, 
	id INTEGER, name TEXT, enemies INTEGER[], friends INTEGER[], issues_disbanded INTEGER[],
	first_issue INTEGER);

CREATE TABLE comicvinedb.team_to_issue (pk SERIAL PRIMARY KEY NOT NULL, 
		team_pk INTEGER, issue_pk INTEGER);
		
CREATE TABLE comicvinedb.power (pk SERIAL PRIMARY KEY NOT NULL, aliases TEXT, 
	description TEXT, id INTEGER, name TEXT, power_class_pk INTEGER);

CREATE TABLE comicvinedb.power_class (pk SERIAL PRIMARY KEY NOT NULL, name TEXT);

CREATE TABLE comicvinedb.species (pk SERIAL PRIMARY KEY NOT NULL, label TEXT);

CREATE TABLE comicvinedb.gender (pk SERIAL PRIMARY KEY NOT NULL, label TEXT);

CREATE TABLE comicvinedb.ethnicity (pk SERIAL PRIMARY KEY NOT NULL, label TEXT);

CREATE TABLE comicvinedb.orientation (pk SERIAL PRIMARY KEY NOT NULL, label TEXT);

CREATE TABLE comicvinedb.issue_to_story_arc (pk SERIAL PRIMARY KEY NOT NULL, 
		issue_pk INTEGER, story_arc_pk INTEGER);
		
CREATE TABLE comicvinedb.story_arc (pk SERIAL PRIMARY KEY NOT NULL, aliases TEXT,
	issue_count INTEGER, deck TEXT, description TEXT, id INTEGER, name TEXT, first_issue INTEGER);

CREATE TABLE comicvinedb.volume (pk SERIAL PRIMARY KEY NOT NULL, aliases TEXT,
	issue_count INTEGER, deck TEXT, description TEXT, id INTEGER, name TEXT,
	start_year INTEGER, publisher_pk INTEGER, first_issue INTEGER, last_issue INTEGER);

CREATE TABLE comicvinedb.publisher (pk SERIAL PRIMARY KEY NOT NULL, aliases TEXT,
	deck TEXT, description TEXT, id INTEGER, name TEXT);

CREATE TABLE comicvinedb.location (pk SERIAL PRIMARY KEY NOT NULL, aliases TEXT,
	issue_count INTEGER, deck TEXT, description TEXT, id INTEGER, name TEXT, 
	first_issue INTEGER, start_year INTEGER);
	
CREATE TABLE comicvinedb.location_to_issue (pk SERIAL PRIMARY KEY NOT NULL, 
	issue_pk INTEGER, location_pk INTEGER);
	
INSERT INTO comicvinedb.orientation VALUES (0,'straight'),(1,'gay'),(2,'lesbian'),(3,'bisexual'),(4,'asexual'),(5,'other');
INSERT INTO comicvinedb.gender VALUES (0, 'male'), (1,'female'), (2,'transgender'),(4,'other');
INSERT INTO comicvinedb.ethnicity VALUES (0,'white'),(1,'black'),(2,'asian'),(3,'latino'),(4,'native american'),(5,'other');
INSERT INTO comicvinedb.alignment VALUES (0, 'hero'), (1,'villain'), (2,'neutral'),(3,'antihero');
INSERT INTO comicvinedb.power_class VALUES (0,'Physical'),(1,'Mental'),(2,'Energy'),(3,'Spacetime'),(4,'Biology'),(5,'Training'),(6,'Technology'),(7,'Magic'),(8,'Elemental'),(9,'Economy');

ALTER TABLE ONLY comicvinedb.character
	ADD CONSTRAINT origin_fk
	FOREIGN KEY (origin_pk) REFERENCES comicvinedb.origin(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY comicvinedb.character
	ADD CONSTRAINT alignment_fk
	FOREIGN KEY (alignment_pk) REFERENCES comicvinedb.alignment(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY comicvinedb.character_to_team
	ADD CONSTRAINT character_fk
	FOREIGN KEY (character_pk) REFERENCES comicvinedb.character(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	

ALTER TABLE ONLY comicvinedb.character_to_team
	ADD CONSTRAINT team_fk
	FOREIGN KEY (team_pk) REFERENCES comicvinedb.team(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY comicvinedb.character_to_power
	ADD CONSTRAINT character_fk
	FOREIGN KEY (character_pk) REFERENCES comicvinedb.character(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	

ALTER TABLE ONLY comicvinedb.character_to_power
	ADD CONSTRAINT power_fk
	FOREIGN KEY (power_pk) REFERENCES comicvinedb.power(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY comicvinedb.character_to_creator
	ADD CONSTRAINT character_fk
	FOREIGN KEY (character_pk) REFERENCES comicvinedb.character(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	

ALTER TABLE ONLY comicvinedb.character_to_creator
	ADD CONSTRAINT creator_fk
	FOREIGN KEY (creator_pk) REFERENCES comicvinedb.creator(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY comicvinedb.character_to_issue
	ADD CONSTRAINT character_fk
	FOREIGN KEY (character_pk) REFERENCES comicvinedb.character(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	

ALTER TABLE ONLY comicvinedb.character_to_issue
	ADD CONSTRAINT issue_fk
	FOREIGN KEY (issue_pk) REFERENCES comicvinedb.issue(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY comicvinedb.character_to_identity
	ADD CONSTRAINT character_fk
	FOREIGN KEY (character_pk) REFERENCES comicvinedb.character(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	

ALTER TABLE ONLY comicvinedb.character_to_identity
	ADD CONSTRAINT identity_fk
	FOREIGN KEY (identity_pk) REFERENCES comicvinedb.identity(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY comicvinedb.creator
	ADD CONSTRAINT gender_fk
	FOREIGN KEY (gender_pk) REFERENCES comicvinedb.gender(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;
		
ALTER TABLE ONLY comicvinedb.power
	ADD CONSTRAINT power_class_fk
	FOREIGN KEY (power_class_pk) REFERENCES comicvinedb.power_class(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY comicvinedb.issue_to_story_arc
	ADD CONSTRAINT issue_fk
	FOREIGN KEY (issue_pk) REFERENCES comicvinedb.issue(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	

ALTER TABLE ONLY comicvinedb.issue_to_story_arc
	ADD CONSTRAINT story_arc_fk
	FOREIGN KEY (story_arc_pk) REFERENCES comicvinedb.story_arc(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;
	
ALTER TABLE ONLY comicvinedb.identity_to_species
	ADD CONSTRAINT identity_fk
	FOREIGN KEY (identity_pk) REFERENCES comicvinedb.identity(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	

ALTER TABLE ONLY comicvinedb.identity_to_species
	ADD CONSTRAINT species_fk
	FOREIGN KEY (species_pk) REFERENCES comicvinedb.species(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;
	
ALTER TABLE ONLY comicvinedb.issue
	ADD CONSTRAINT volume_fk
	FOREIGN KEY (volume_pk) REFERENCES comicvinedb.volume(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;
	
ALTER TABLE ONLY comicvinedb.volume
	ADD CONSTRAINT publisher_fk
	FOREIGN KEY (publisher_pk) REFERENCES comicvinedb.publisher(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;		
	
ALTER TABLE ONLY comicvinedb.identity
	ADD CONSTRAINT gender_fk
	FOREIGN KEY (gender_pk) REFERENCES comicvinedb.gender(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	

ALTER TABLE ONLY comicvinedb.identity
	ADD CONSTRAINT ethnicity_fk
	FOREIGN KEY (ethnicity_pk) REFERENCES comicvinedb.ethnicity(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;
	
ALTER TABLE ONLY comicvinedb.identity
	ADD CONSTRAINT orientation_fk
	FOREIGN KEY (orientation_pk) REFERENCES comicvinedb.orientation(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	

ALTER TABLE ONLY comicvinedb.team_to_issue
	ADD CONSTRAINT team_fk
	FOREIGN KEY (team_pk) REFERENCES comicvinedb.team(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	

ALTER TABLE ONLY comicvinedb.team_to_issue
	ADD CONSTRAINT issue_fk
	FOREIGN KEY (issue_pk) REFERENCES comicvinedb.issue(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	
	
ALTER TABLE ONLY comicvinedb.creator_to_issue
	ADD CONSTRAINT creator_fk
	FOREIGN KEY (creator_pk) REFERENCES comicvinedb.creator(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	

ALTER TABLE ONLY comicvinedb.creator_to_issue
	ADD CONSTRAINT issue_fk
	FOREIGN KEY (issue_pk) REFERENCES comicvinedb.issue(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;
			
ALTER TABLE ONLY comicvinedb.location_to_issue
	ADD CONSTRAINT issue_fk
	FOREIGN KEY (issue_pk) REFERENCES comicvinedb.issue(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;
	
ALTER TABLE ONLY comicvinedb.location_to_issue
	ADD CONSTRAINT location_fk
	FOREIGN KEY (location_pk) REFERENCES comicvinedb.location(pk)
	ON UPDATE CASCADE ON DELETE CASCADE;	
	
			