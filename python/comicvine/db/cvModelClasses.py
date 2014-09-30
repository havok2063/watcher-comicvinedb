#!/usr/bin/python

# -------------------------------------------------------------------
# Import statements
# -------------------------------------------------------------------
import sys, math, os, datetime
from decimal import *

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relationship, exc, column_property
from sqlalchemy import orm
from sqlalchemy.orm.session import Session
from sqlalchemy import String # column types, only used for custom type definition
from sqlalchemy import func # for aggregate, other functions

from comicvine.db.DatabaseConnection import DatabaseConnection

db = DatabaseConnection()

# ========================
# Define database classes
# ========================
Base = db.Base

class Alignment(Base):
    __tablename__ = 'alignment'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Alignment (pk={0},label={1})>'.format(self.pk,self.label)

class Character(Base):
    __tablename__ = 'character'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Character (pk={0},name={1})>'.format(self.pk,self.name)
    
    def teamFriends(self):
        
        session = Session.object_session(self)
        teamlist = []
        for team in self.team_friends:
            try: team = session.query(Team).filter_by(id=team).one()
            except TypeError: team = None
            except sqlalchemy.orm.exc.NoResultFound: team = None
            teamlist.append(team)
        return teamlist   

    def teamEnemies(self):
        
        session = Session.object_session(self)
        teamlist = []
        for team in self.team_enemies:
            try: team = session.query(Team).filter_by(id=team).one()
            except TypeError: team = None
            except sqlalchemy.orm.exc.NoResultFound: team = None
            teamlist.append(team)
        return teamlist        

    def Friends(self):
        
        session = Session.object_session(self)
        friends = []
        for friend in self.friends:
            try: friend = session.query(Character).filter_by(id=friend).one()
            except TypeError: friend = None
            except sqlalchemy.orm.exc.NoResultFound: friend = None
            friends.append(friend)
        return friends   

    def Enemies(self):
        
        session = Session.object_session(self)
        enemies = []
        for team in self.team_enemies:
            try: team = session.query(Character).filter_by(id=enemy).one()
            except TypeError: enemy = None
            except sqlalchemy.orm.exc.NoResultFound: enemy = None
            enemies.append(enemy)
        return enemies     
                                  
class CharacterToTeam(Base):
    __tablename__ = 'character_to_team'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<CharacterToTeam (pk={0},character_pk={1}, team_pk={2})>'.format(self.pk,self.character_pk,self.team_pk)
        
class CharacterToPower(Base):
    __tablename__ = 'character_to_power'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<CharacterToPower (pk={0},character_pk={1}, power_pk={2})>'.format(self.pk,self.character_pk,self.power_pk)

class CharacterToCreator(Base):
    __tablename__ = 'character_to_creator'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<CharacterToCreator (pk={0},character_pk={1}, creator_pk={2})>'.format(self.pk,self.character_pk,self.creator_pk)

class CharacterToIdentity(Base):
    __tablename__ = 'character_to_identity'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<CharacterToIdentity (pk={0},character_pk={1}, identity_pk={2})>'.format(self.pk,self.character_pk,self.identity_pk)

class CharacterToIssue(Base):
    __tablename__ = 'character_to_issue'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<CharacterToIssue (pk={0},character_pk={1}, issue_pk={2})>'.format(self.pk,self.character_pk,self.issue_pk)

class Creator(Base):
    __tablename__ = 'creator'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Creator (pk={0},name={1})>'.format(self.pk,self.name) 
        
class CreatorToIssue(Base):
    __tablename__ = 'creator_to_issue'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<CreatorToIssue (pk={0},creator_pk={1}, issue_pk={2})>'.format(self.pk,self.creator_pk,self.issue_pk)

class Ethnicity(Base):
    __tablename__ = 'ethnicity'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Ethnicity (pk={0},label={1})>'.format(self.pk,self.label)

class Gender(Base):
    __tablename__ = 'gender'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Gender (pk={0},label={1})>'.format(self.pk,self.label)
                
class Identity(Base):
    __tablename__ = 'identity'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Identity (pk={0},name={1})>'.format(self.pk,self.name)

class IdentityToSpecies(Base):
    __tablename__ = 'identity_to_species'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<IdentityToSpecies (pk={0},identity_pk={1}, species_pk={2})>'.format(self.pk,self.identity_pk,self.species_pk)

class Issue(Base):
    __tablename__ = 'issue'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Issue (pk={0},name={1})>'.format(self.pk,self.name)

class IssueToStoryArc(Base):
    __tablename__ = 'issue_to_story_arc'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<IssueToStoryArc (pk={0},issue_pk={1}, story_arc_pk={2})>'.format(self.pk,self.issue_pk,self.story_arc_pk)

class Location(Base):
    __tablename__ = 'location'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Location (pk={0},name={1})>'.format(self.pk,self.name)
 
class LocationToIssue(Base):
    __tablename__ = 'location_to_issue'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<LocationToIssue (pk={0},issue_pk={1}, location_pk={2})>'.format(self.pk,self.issue_pk,self.location_pk)

class Orientation(Base):
    __tablename__ = 'orientation'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Orientation (pk={0},label={1})>'.format(self.pk,self.label)
        
class Origin(Base):
    __tablename__ = 'origin'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Origin (pk={0},name={1})>'.format(self.pk,self.name)
  
class Power(Base):
    __tablename__ = 'power'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Power (pk={0},name={1})>'.format(self.pk,self.name)
  
class PowerClass(Base):
    __tablename__ = 'power_class'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<PowerClass (pk={0},name={1})>'.format(self.pk,self.name)

class Publisher(Base):
    __tablename__ = 'publisher'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Publisher (pk={0},name={1})>'.format(self.pk,self.name)

class Species(Base):
    __tablename__ = 'species'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Species (pk={0},label={1})>'.format(self.pk,self.label)
  
class StoryArc(Base):
    __tablename__ = 'story_arc'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<StoryArc (pk={0},name={1})>'.format(self.pk,self.name)
      
class Team(Base):
    __tablename__ = 'team'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Team (pk={0},name={1})>'.format(self.pk,self.name)

class TeamToIssue(Base):
    __tablename__ = 'team_to_issue'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<TeamToIssue (pk={0},team_pk={1}, issue_pk={2})>'.format(self.pk,self.team_pk,self.issue_pk)

class Volume(Base):
    __tablename__ = 'volume'
    __table_args__ = {'autoload' : True, 'schema' : 'comicvinedb'}
    
    def __repr__(self):
        return '<Volume (pk={0},name={1})>'.format(self.pk,self.name)
      
# ========================
# Define relationships
# ========================

Character.issues = relationship(Issue, secondary=CharacterToIssue.__table__, backref='characters')
Character.teams = relationship(Team, secondary=CharacterToTeam.__table__, backref='characters')
Character.powers = relationship(Power, secondary=CharacterToPower.__table__, backref='characters')
Character.creators = relationship(Creator, secondary=CharacterToCreator.__table__, backref='characters')
Character.identities = relationship(Identity, secondary=CharacterToIdentity.__table__, backref='characters')
Character.alignment = relationship(Alignment, backref='characters')
Character.origin = relationship(Origin, backref='characters')

Creator.gender = relationship(Gender, backref='creators')

Identity.species = relationship(Species, secondary=IdentityToSpecies.__table__, backref='identities')
Identity.gender = relationship(Gender, backref='identities')
Identity.ethnicity = relationship(Ethnicity, backref='identities')

Issue.creators = relationship(Creator, secondary=CreatorToIssue.__table__, backref='issues')
Issue.teams = relationship(Team, secondary=TeamToIssue.__table__, backref='issues')
Issue.storyarcs = relationship(StoryArc, secondary=IssueToStoryArc.__table__, backref='issues')
Issue.volume = relationship(Volume, backref='issues')
Issue.locations = relationship(Location, secondary=LocationToIssue.__table__, backref='issues')

Power.powerclass = relationship(PowerClass, backref='powers')
Volume.publisher = relationship(Publisher, backref='volumes')


  
# ---------------------------------------------------------
# Test that all relationships/mappings are self-consistent.
# ---------------------------------------------------------
from sqlalchemy.orm import configure_mappers
try:
	configure_mappers()
except RuntimeError, error:
	print """
mangadb.ModelClasses:
An error occurred when verifying the relationships between the database tables.
Most likely this is an error in the definition of the SQLAlchemy relationships - 
see the error message below for details.
"""
	print "Error type: %s" % sys.exc_info()[0]
	print "Error value: %s" % sys.exc_info()[1]
	print "Error trace: %s" % sys.exc_info()[2]
	sys.exit(1)

         
    