# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:36:45 2017

@author: Rachit
"""

from flask import Flask

application = Flask(__name__)
application.config.from_object('config')

from application import views
