#!/usr/bin/python

import os

import flask
from flask import request, render_template, send_from_directory, current_app

from ..model.database import db

import comicvine.db.cvModelClasses as cvdb

xmatch_page = flask.Blueprint("xmatch_page", __name__)

@xmatch_page.route('/xmatch.html', methods=['GET'])
def xmatch():
    ''' Documentation here. '''
    
    session = db.Session()
    
    xmatchDict = {}


    return render_template("xmatch.html", **xmatchDict)

