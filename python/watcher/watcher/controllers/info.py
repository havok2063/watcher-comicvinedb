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
    
    name = valueFromRequest(key="name", request=request, default=None)

    try:
        character = session.query(cvdb.Character).filter_by(name=name).one()
    except sqlalchemy.orm.exc.NoResultFound:
        character = None
    infoDict['character'] = character
    infoDict['name']=name
        
    #compute issue/time ratio
    nowyear = datetime.datetime.now().year
    firstyear = 1960.
    timespan = nowyear-firstyear
    ratio = character.issue_count/timespan if character else None
    infoDict['ratio'] = ratio
    
    #powers
    powers = character.powers if character else None
    powclass = []
    powertree = {'name':'Powers','children':powclass}

    return render_template("info.html", **infoDict)

