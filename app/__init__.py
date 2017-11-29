# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:36:45 2017

@author: Rachit
"""

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views
