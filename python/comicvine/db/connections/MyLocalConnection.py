#!/usr/bin/python

import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from ..DatabaseConnection import DatabaseConnection

# ---------------------------------------------
# Fill in database connection information here.
# ---------------------------------------------
db_config = {
	'user'     : 'cvadmin',     # specify the database username
	'password' : '',     # the database password for that user
	'database' : 'comicvinedb', 		 	 # the name of the database
	'host'     : 'localhost', # your hostname, "localhost" if on your own machine
	'port'     : 5432
}

database_connection_string = 'postgresql://{0[user]}:{0[password]}@{0[host]}:{0[port]}/{0[database]}'.format(db_config)

# This allows the file to be 'import'ed any number of times, but attempts to
# connect to the database only once.
try:
	db = DatabaseConnection() # fails if connection not yet made.
except:
	db = DatabaseConnection(database_connection_string=database_connection_string)

engine = db.engine
metadata = db.metadata
#Session = sessionmaker(bind=engine, autocommit=True, autoflush=False)
Session = scoped_session(sessionmaker(bind=engine, autocommit=True, autoflush=False))

