#!/usr/bin/python

import os

import flask, sqlalchemy
from flask import request, render_template, send_from_directory, current_app

from ..model.database import db

import comicvine.db.cvModelClasses as cvdb
import datetime

try:
    from . import valueFromRequest
except ValueError:
    pass 
    
info_page = flask.Blueprint("info_page", __name__)

@info_page.route('/info.html', methods=['GET'])
def info():
    ''' Documentation here. '''
    
    session = db.Session()
    infoDict = {}
    jsDict = {}
    
    # Grab character name from GET request
    name = valueFromRequest(key="name", request=request, default=None)

	# Grab character from database
    try:
        character = session.query(cvdb.Character).filter_by(name=name).one()
    except sqlalchemy.orm.exc.NoResultFound:
        character = None
    infoDict['character'] = character
    infoDict['name']=name
    
    if character:    
        #compute issue/time ratio
        nowyear = datetime.datetime.now().year
        firstyear = 1960.
        timespan = nowyear-firstyear
        ratio = character.issue_count/timespan if character else None
        infoDict['ratio'] = ratio
    
        #get powers
        powers = character.powers if character else None
        pcclass = [p.powerclass for p in powers]
        powclass =[{'name':p.name,'parent':'Powers','children':[{'parent':p.name,'name':pow.name} for pow in character.powers if pow.powerclass.name==p.name]} for p in list(set(pcclass))]
        powertree = [{'name':'Powers','parent':'null','children':powclass}]
        jsDict['powertree']=powertree

	# Render javascript template, and add it to the main template
	js = render_template('powertree.js', **jsDict)
	infoDict['js']=js
	
    return render_template("info.html", **infoDict)

