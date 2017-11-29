# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:45:47 2017

@author: Rachit
"""

from flask import render_template, flash, redirect, request
from flask import Markup
from app import app
from .forms import ReusableForm
from .Tweet_ana_1 import tweets_senti
from .Election_tweets import electionTweets
# from markupsafe import Markup
from plotly.offline import plot
from plotly.graph_objs import Scatter
# index view function suppressed for brevity

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    form = ReusableForm()
    if request.method == 'POST':
        name=request.form['name']
        # print name
        # flash('Hello ' + name)
        tweets_senti_obj = tweets_senti()
        basic_scatter_string,scatter_ids,basic_bar_string, bar_ids,basic_map_string, map_ids  = tweets_senti_obj.search_tweets(name)
        # basic_scatter_string = plot([Scatter(x=[1, 2, 3], y=[3, 1, 6])], output_type='div',include_plotlyjs=False)
        return render_template('hello.html', form=form,
                               scatterPlot = basic_scatter_string,
                               scatter_ids = scatter_ids,
                               barPlot = basic_bar_string,bar_ids=bar_ids,
                               mapPlot = basic_map_string, map_ids = map_ids)
#==============================================================================
#         if form.validate():
#             # Save the comment here.
#             flash('Hello ' + name)
#         else:
#             flash('All the form fields are required. ')
#==============================================================================
 
    return render_template('hello.html', form=form)

@app.route('/electionresults', methods=['GET'])
def election_Tweets():
    elect_tweets = electionTweets()
    print("Inside")
    basic_scatter_string,scatter_ids,basic_bar_string, bar_ids,basic_map_string, map_ids = elect_tweets.cal_election("ABC.txt")
    return render_template('electionResults.html',scatterPlot = basic_scatter_string,
                               scatter_ids = scatter_ids,
                               barPlot = basic_bar_string,bar_ids=bar_ids,
                               mapPlot = basic_map_string, map_ids = map_ids)