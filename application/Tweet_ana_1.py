class tweets_senti():
#import plotly
#plotly.tools.set_credentials_file(username='rkpabreja', api_key='YFoURDgLa26Y2prwawE7')

#==============================================================================
#     import plotly.plotly as py
#     from plotly.graph_objs import *
#     plotly.tools.set_credentials_file(username='rkpabreja', api_key='YFoURDgLa26Y2prwawE7')
#     
#     mapbox_access_token = 'pk.eyJ1IjoicmtwYWJyZWphIiwiYSI6ImNqOW5idW5uZTR5Y2EzMm5yNDNtN3FkMDIifQ.qnxzKIox7JFIRXlNzbeYkQ'
#==============================================================================
    def search_tweets(self, q):
        import pandas as pd
        from twitter import Twitter 
        from twitter import OAuth 
        from pandas.io.json import json_normalize
        from twitter import TwitterHTTPError
        
        ACCESS_TOKEN = '136600388-9iihe7SFq8nZUOL5GjxoZlPbxW2MYcScWlZ6sD3a'
        ACCESS_SECRET = 'ScmAR4iYHCxuPHhYMifirTK0h2Jhdqt1p10uoz9lHTshT'
        consumer_key = 'bto0MsRvjjfkrl4QpndjaUneg'
        consumer_secret = '5zr7Xr9y4AbKgUCuWRmQGaMvizwg48HpVeyjbSZC4j350rIYPF'
    
        oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, consumer_key, consumer_secret)
        twitter = Twitter(auth=oauth)
        #q = 'modi'
        count = 100
        
        search_results = twitter.search.tweets(q=q,count = count)
        Original_status_df = json_normalize(search_results,['statuses'])
        Original_status_df = pd.DataFrame(Original_status_df)
        min_id = min(Original_status_df['id'])
        max_id = max(Original_status_df['id'])
        # Original_status_df.to_csv("E:/MIT/Fall2k17/Capstone/tweets.csv")
        while len(Original_status_df) < 300:
        #while min_id is not None:
             #print(min_id)
             try:
                 search_results = twitter.search.tweets(q=q,count=count,max_id = min_id)
                 results = json_normalize(search_results,['statuses'])
                 Original_status_df = Original_status_df.append(results)
                 min_id = min(results['id'])
                 max_id = max(results['id'])
                 #print(Original_status_df.shape)
             except TwitterHTTPError:
                 break
        
        Original_status_df = Original_status_df.reset_index()
        tweet_df = cleanTweets(Original_status_df)
        tweet_df_live_sentiments = cal_sentiment(tweet_df)
        basic_scatter_string,scatter_ids = plot_sentiments(tweet_df_live_sentiments['Polarity'],tweet_df_live_sentiments['Subjectivity'],tweet_df_live_sentiments['Reputation'])
        
        bar_df = tweet_df_live_sentiments[['Polarity','Subjectivity','created_at']]
        times =pd.to_datetime(bar_df['created_at'])
        bar_df.index = times
        bar_df = bar_df.resample('T').mean()
        #bar_df_sentiments= bar_df.groupby(times.dt.hour)[['Polarity','Subjectivity']].mean()
        #bar_df_sentiments_min= bar_df.groupby([times.dt.date,times.dt.hour,times.dt.minute])[['Polarity','Subjectivity']].mean()
        #basic_bar_string = bar_sentiments(bar_df_sentiments['Polarity'],bar_df_sentiments['Subjectivity'],bar_df_sentiments.index)
        basic_bar_string, bar_ids = bar_sentiments(bar_df['Polarity'],bar_df['Subjectivity'],bar_df.index)
        #basic_bar_string =  = bar_sentiments()
        map_df = tweet_df_live_sentiments[['Polarity','US_State_of_tweet']]
        map_df = map_df.groupby('US_State_of_tweet').mean()
        basic_map_string, map_ids = map_plot(map_df['Polarity'],map_df.index)
        world_map_df = tweet_df_live_sentiments[['Polarity','Country_of_tweet']]
        world_map_df = world_map_df.groupby('Country_of_tweet').mean()
        world_map_string, world_map_ids = world_map(world_map_df['Polarity'], world_map_df.index)
        return basic_scatter_string,scatter_ids,basic_bar_string,bar_ids,basic_map_string, map_ids,world_map_string, world_map_ids
        
    # read csv file from ussama     


# read_tweets_csv('E:/MIT/Fall2k17/Capstone/Twitter_analysis/output27.csv')

def cleanTweets(tweet_df):
    import re
    status_row = []
    for i in range(len(tweet_df)):
        status_ = tweet_df.iloc[i,:]['text'].lower()
        status_ = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',status_)
        status_ = re.sub('@[^\s]+','',status_)
        status_ = re.sub('[^A-Za-z0-9 ]+', '', status_)
        status_ = status_.replace('rt','')
        status_row.append(status_)
    tweet_df['text'] = status_row
    list_drop = ['contributors','geo','extended_entities','source','in_reply_to_screen_name', 'in_reply_to_status_id',
       'in_reply_to_status_id_str', 'in_reply_to_user_id',
       'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'metadata','quoted_status_id',
       'quoted_status_id_str','possibly_sensitive','quoted_status']
    list_to_drop = list(set(list_drop).intersection(tweet_df.columns)) 
    tweet_df = tweet_df.drop(list_to_drop,axis=1)
    list1 = []
    for i in range(len(tweet_df)):
        list1.append(tweet_df.iloc[i,:]['user']['location'])
        
    tweet_df['location_of_tweet'] = list1
    tweet_df = Country_of_tweet(tweet_df)
    tweet_df = US_State_of_tweet(tweet_df)
    tweet_df = Updated_country_of_tweet(tweet_df)
    return tweet_df

countries_filter = ['Bangladesh','Canada','Dubai','Kenya''Nigeria','Prague','Argentina','Thailand','Italy','India','Pakistan',
                    'United States','Germany','Spain','France','China','Mexico','Japan','Brasil','Brazil','United Arab Emirates',
                    'UAE','Australia','Portugal','South Africa','Russia','Chile','United Kingdom','Indonesia','Philippines','USA']

def Country_of_tweet(dataframe):
    list3 =[]
    country_names_updated = {'Prague' : 'Czechia','United States':'USA'}
    for i in range(len(dataframe)):
        setblank =0
        location = dataframe.iloc[i,:]['location_of_tweet']
        for country in countries_filter:
            if(country in location or country.lower() in location or country.upper() in location):
                country_updated = country_names_updated.get(country,country)
                list3.append(country_updated) 
                setblank = 1
                break
        if(setblank == 0):
            list3.append("")
        
    dataframe['Country_of_tweet'] = list3
    return dataframe

us_city_state_filter =['Albuquerque','Asheville','Atlanta','Austin','Baltimore','Boston','Columbia','Dallas','Detroit','Denver',
                 'Las Vegas','Georgia','Miami','Oklahoma','Los Angeles','Richmond',
                 'San Jose','Seattle','Orlando','Pittsburgh','Texas','San Diego','Chicago',
                 'New York','Phoenix','Mount Prospect','Arizona',
                       'California','Florida','Oregon',
                'Maryland','Michigan','NewJersey','Massachusetts','Missouri','Kentucky','Ohio','New Mexico',
                       'Utah','Virginia','CA','CT','FL','KY','PA','NJ','NY','MI','TX','RI','WA']

def US_State_of_tweet(dataframe):
    import re
    import us
    dummylist =[]
    count = 0
    city_to_state_names_updated = {'Albuquerque':'New Mexico',
                            'Atlanta':'Georgia',
                            'Austin':'Texas',
                                   'Baltimore':'Maryland',
                           'Boston':'Massachusetts',
                           'Columbia':'Missouri',
                                   'Diego':'California',
                           'Denver':'Colorado',
                           'Detroit':'Michigan',
                            'Las Vegas' : 'Nevada',
                                   'Vegas':'Nevada',
                           'Oklahoma':'Oklahoma',
                            'Dallas': 'Texas',
                            'Seattle': 'Washington',
                           'Los Angeles' : 'California',
                            'Orlando': 'Florida',
                            'San Diego' : 'California',
                            'San Jose':'California',
                                   'Jose':'California',
                           'Pittsburgh':'Pennsylvania',
                            'Chicago':'Illinois',
                            'Phoenix':'Arizona',
                           'Richmond':'Virginia',
                          'Mount Prospect':'Illinois',
                          'Maryland':'Virginia',
                          'New Jersey':'New Jersey',
                          'Miami':'Florida',
                          'Asheville':'North Carolina',
                           'Missouri':'Missouri',
                          'New Mexico':'New Mexico',
                                   'AZ':'Arizona',
                                   'CA':'California',
                                   'CT':'Conneticut',
                                   'FL':'Florida',
                                   'IL':'Illinois',
                                   'KY':'Kentucky',
                                   'OR':'Oregon',
                                   'PA':'Pennsylvania',
                                   'GA':'Georgia',
                                   'MA':'Massachusetts',
                                   'MD':'Maryland',
                                   'MI':'Michigan',
                                  'NY':'New York',
                                  'TX':'Texas',
                                  'NJ':'New Jersey',
                                   'NV':'Nevada',
                                  'RI':'Rhode Island',
                                  'WA':'Washington'}
    for i in range(len(dataframe)):
        setblank =0
        location_string =  dataframe.iloc[i,:]['location_of_tweet']
        location_string_split= re.split(r'[,\s]', location_string)
        
        for city_state in us_city_state_filter:
            if(city_state in location_string_split or city_state.lower() in location_string_split or city_state.upper() in location_string_split):
                state_updated = city_to_state_names_updated.get(city_state,city_state)
                dummylist.append(state_updated) 
                setblank = 1
                break
            elif('New York' in city_state or 'Las Vegas' in city_state or 'Los Angeles' in city_state or 'San Fransisco' in city_state):
                if(re.search(city_state,location_string)):
                    state_updated = city_to_state_names_updated.get(city_state,city_state)
                    dummylist.append(state_updated) 
                    setblank = 1
                    break
        if(setblank == 0):
            dummylist.append("")
     
    final_list = []
    map_states_codes = us.states.mapping('name','abbr')
    for i in range(len(dummylist)):
        final_list.append(map_states_codes.get(dummylist[i]))
    
    dataframe['US_State_of_tweet'] = final_list
    return dataframe

import pycountry as pyc
world_dict = dict()
world_dict['']=''
world_dict['USA'] = 'USA'
world_dict['Dubai'] = 'UAE'
world_dict['Russia'] = 'RUS'
for country in pyc.countries:
    country_code = country.alpha_3
    country_name = country.name
    world_dict[country_name] = country_code
def Updated_country_of_tweet(dataframe):
    countrylist = []
    for i in range(len(dataframe)):
        if(dataframe.iloc[i,:]['US_State_of_tweet']is not None):
            countrylist.append('USA')
        else:
            try:
                country = dataframe.iloc[i,:]['Country_of_tweet']
                countrylist.append(world_dict[country])
            except KeyError:
                countrylist.append('')
            
    dataframe['Country_of_tweet'] = countrylist
    return  dataframe

def cal_sentiment(tweet_df):
    from textblob import TextBlob
    polarity = []
    subjectivity = []
    reputation = []
    for i in range(len(tweet_df)):
        wiki = TextBlob(tweet_df.iloc[i,:]['text'])
        polarity.append(wiki.sentiment.polarity)
        subjectivity.append(wiki.sentiment.subjectivity)
        try:
            reputation.append(int(tweet_df.iloc[i,:]['user']['followers_count'])/(int(tweet_df.iloc[i,:]['user']['followers_count'])
            + int(tweet_df.iloc[i,:]['user']['friends_count'])))
        except ValueError:
            reputation.append(0)
        except ZeroDivisionError:
            reputation.append(0)
    tweet_df['Polarity'] = polarity
    tweet_df['Subjectivity']= subjectivity
    tweet_df['Reputation'] = reputation
    tweet_df['Reputation'] = round(tweet_df['Reputation'],1)
    return tweet_df



def plot_sentiments(polarity,subjectivity,reputation):
    #import plotly.offline as offline
    import plotly
    import json
    #plotly.tools.set_credentials_file(username='rkpabreja', api_key='YFoURDgLa26Y2prwawE7')
    #import plotly.plotly as py
    #import plotly.graph_objs as go
#==============================================================================
#     trace = go.Scatter(
#     x = polarity,
#     y = subjectivity,
#     mode = 'markers'
#     )
#     data = [trace]
#==============================================================================
    #obj = py.iplot(data, filename='basic-scatter')
    #basic_scatter_string = obj.embed_code
    text_string = []
    for i in reputation:
        text_string.append('Reputation:'+str(i))
    graphs = [
        dict(
            data=[
                dict(
                    x=polarity,
                    y=subjectivity,
                    type='scatter',
                    mode = 'markers',
                    text = text_string,
                    marker=dict(
                        size='16',
                        color = reputation, #set color equal to a variable
                        colorscale='Viridis',
                        showscale=True
                    )
                ),
            ],
            layout=dict(
                title='Scatter Plot: Polarity vs Subjectivity'
            )
        )]
    scatter_id = ['Scatter']
    basic_scatter_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return basic_scatter_json,scatter_id



def bar_sentiments(polarity,subjectivity,dates):
    import plotly
    import json
    
#==============================================================================
#     trace1 = go.Bar(
#         x=dates,
#         y=polarity,
#         name='Polarity'
#     )
#     trace2 = go.Bar(
#         x=dates,
#         y=subjectivity,
#         name='Subjectivity'
#     )
#     
#     data = [trace1, trace2]
#     layout = go.Layout(
#         barmode='group'
#     )
#==============================================================================
    graphs = [
        dict(
            data=[
                dict(
                    x=dates,
                    y=polarity,
                    type='bar',
                    name='Polarity'
                ),
				dict(
                    x=dates,
                    y=subjectivity,
                    type='bar',
                    name='Subjectivity'
                ),
            ],
            layout=dict(
                title='Bar Plot',
                barmode='group',
                bargap=0.15,
                bargroupgap=0.1
            )
        )]
    bar_id = ['Bar']
    basic_bar_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
#==============================================================================
#     fig = go.Figure(data=data, layout=layout)
#     basic_bar_string = offline.plot(fig,auto_open=False,include_plotlyjs=False, output_type='div')
#==============================================================================
    return basic_bar_json,bar_id
    #py.plot(fig, filename='grouped-bar')
    
#==============================================================================
#     bar_df = Original_status_df[['Polarity','Subjectivity','created_at']]
#     times =pd.to_datetime(bar_df['created_at'])
#     bar_df_sentiments= bar_df.groupby(times.dt.hour)[['Polarity','Subjectivity']].mean()
#     bar_df_sentiments_min= bar_df.groupby(times.dt.minute)[['Polarity','Subjectivity']].mean()
#     bar_sentiments(bar_df_sentiments['Polarity'],bar_df_sentiments['Subjectivity'],bar_df_sentiments.index)
#     bar_sentiments(bar_df_sentiments_min['Polarity'],bar_df_sentiments_min['Subjectivity'],bar_df_sentiments_min.index)
#     
#     coordinates_df = Original_status_df[Original_status_df.coordinates.notnull()]
#     coordinate_df = coordinates_df['coordinates']
#     lat = []
#     long = []
#     for i in range(len(coordinate_df)):
#         coor_ = coordinate_df.iloc[i]
#         lat_,long_ = coor_.get('coordinates')
#         lat.append(lat_)
#         long.append(long_)
#     
#     coordinates_df['Latitude'] = lat
#     coordinates_df['Longitude'] = long
#==============================================================================
def map_plot(polarity,us_state_code):
    import plotly
    import json
    scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
    graphs = [
        dict(
            data = [ dict(
                        type='choropleth',
                        colorscale = scl,
                        autocolorscale = False,
                        locations = us_state_code,
                        z = polarity,
                        locationmode = 'USA-states',
                        marker = dict(
                            line = dict (
                                color = 'rgb(255,255,255)',
                                width = 2
                            ) ),
                        colorbar = dict(
                            title = "Map Plot")
                        )
                    ],
            layout = dict(
            title = 'Map Plot',
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)'),
                 )
            )
            ]
    map_id = ['Map']
    basic_map_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return basic_map_json, map_id

def world_map(polarity,country_code):
    import plotly
    import json
#==============================================================================
#     scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
#             [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
#==============================================================================
    graphs = [
        dict(
            data = [ 
                    dict(
                        type = 'choropleth',
                        locations = country_code,
                        z = polarity,
                        text = country_code,
                        colorscale = [[-1,"rgb(5, 10, 172)"],[-0.5,"rgb(40, 60, 190)"],[0.0,"rgb(70, 100, 245)"],\
                            [0.3,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
                        autocolorscale = False,
                        reversescale = True,
                        marker = dict(
                            line = dict (
                                color = 'rgb(180,180,180)',
                                width = 0.5
                            ) ),
                        colorbar = dict(
                            autotick = False,
                            title = 'Polarity'),
                      )
                    ],
            layout = dict(
            title = 'World Map Plot',
            geo = dict(
                showframe = False,
                showcoastlines = True,
                projection = dict(
                    type = 'Mercator'
                )
                )   
            )
        )
    ]
    world_map_id = ['World_Map']
    world_map_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return world_map_json, world_map_id