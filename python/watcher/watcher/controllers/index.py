#!/usr/bin/python

import os

import flask
from flask import request, render_template, send_from_directory, current_app

from ..model.database import db

import comicvine.db.cvModelClasses as cvdb

index_page = flask.Blueprint("index_page", __name__)

@index_page.route('/', methods=['GET'])
def index():
    ''' Documentation here. '''
    
    session = db.Session()
    
    indexDict = {}


    return render_template("index.html", **indexDict)
