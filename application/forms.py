# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:45:47 2017

@author: Rachit
"""

from flask_wtf import Form
from wtforms import StringField, BooleanField,TextField, validators
from wtforms.validators import DataRequired

class ReusableForm(Form):
    name = TextField('Keyword:', validators=[validators.required()])