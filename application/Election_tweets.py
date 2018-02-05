import pandas as pd
class electionTweets():
    def cal_election(self,filename):
        # read_tweets_csv('E:/MIT/Fall2k17/Capstone/Twitter_analysis/output27.csv')
#==============================================================================
#         tweet_df_passive = clean_tweets('E:/MIT/Fall2k17/Capstone/Twitter_analysis/output27.txt')
#         tweet_df_passive = cleanTweets(tweet_df_passive)
#         basic_scatter_string,scatter_ids = plot_sentiments(tweet_df_passive['Polarity'],tweet_df_passive['Subjectivity'],tweet_df_passive['Reputation'])
#         scatter_file = open("E:/MIT/Fall2k17/Capstone/Twitter_analysis/scatter.txt","w")
#         scatter_file.write(basic_scatter_string)
#==============================================================================
        scatt_file = open("E:/MIT/Fall2k17/Capstone/Twitter_analysis/scatter.txt","r")        
        basic_scatter_string = scatt_file.read()
        scatter_ids = ['Scatter']
        
#==============================================================================
#         bar_df = tweet_df_passive[['Polarity','Subjectivity','Date']]
#         times =pd.to_datetime(bar_df['Date'])
#         bar_df.index = times
#         bar_df = bar_df.resample('T').mean()
#         basic_bar_string, bar_ids = bar_sentiments(bar_df['Polarity'],bar_df['Subjectivity'],bar_df.index)
#         bar_file = open("E:/MIT/Fall2k17/Capstone/Twitter_analysis/bar.txt","w")
#         bar_file.write(basic_bar_string)
#==============================================================================
        bar_file = open("E:/MIT/Fall2k17/Capstone/Twitter_analysis/bar.txt","r")        
        basic_bar_string = bar_file.read()
        bar_ids = ['Bar']
        
#==============================================================================
#         map_df = tweet_df_passive[['Polarity','US_State_of_tweet']]
#         map_df = map_df.groupby('US_State_of_tweet').mean()
#         basic_map_string, map_ids = map_plot(map_df['Polarity'],map_df.index)
#         map_file = open("E:/MIT/Fall2k17/Capstone/Twitter_analysis/map.txt","w")
#         map_file.write(basic_map_string)
#==============================================================================
        map_file = open("E:/MIT/Fall2k17/Capstone/Twitter_analysis/map.txt","r")        
        basic_map_string = map_file.read()
        map_ids = ['Map']
#==============================================================================
#         world_map_df = tweet_df_passive[['Polarity','Country_of_tweet']]
#         world_map_df = world_map_df.groupby('Country_of_tweet').mean()
#         world_map_string, world_map_ids = world_map(world_map_df['Polarity'], world_map_df.index)
#         worldmap_file = open("E:/MIT/Fall2k17/Capstone/Twitter_analysis/worldmap.txt","w")
#         worldmap_file.write(world_map_string)
#==============================================================================
        worldmap_file = open("E:/MIT/Fall2k17/Capstone/Twitter_analysis/worldmap.txt","r")        
        world_map_string = worldmap_file.read()
        world_map_ids =  ['World_Map']
        return basic_scatter_string,scatter_ids, basic_bar_string,bar_ids,basic_map_string, map_ids,world_map_string, world_map_ids
        #return basic_scatter_string,scatter_ids
    
def read_tweets_csv(filename):
    import csv
    from datetime import datetime
    
    f = open(filename)
    csv_f = csv.reader(f)
    fil_split = filename.split('/')
    name = fil_split[len(fil_split) - 1].split('.')[0]
    output = open('E:/MIT/Fall2k17/Capstone/Twitter_analysis/' + name + '.txt', 'w')
    # writer = csv.writer(output, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    
    totalrows=0
    
    
    for row in csv_f:    
            if len(row)>30:
                #if totalrows > 154000:
                #    break
                #else:
                a=3
                row_new = row[0][15:-1]
                row_text = row[3][5:]
                d=datetime.strptime(row_new,'%a %b %d %H:%M:%S +0000 %Y')
                # print(d.strftime('%Y-%m-%d %H:%M:%S'))
                print(totalrows)
                if len(row[3])<200:
                        print(output.write(d.strftime('%Y-%m-%d %H:%M:%S') + "\t" +row_text+"\t"))
                        totalrows=totalrows+1
                        if row[a+1][:7]=='display':
                                a=a+2
                   
                        print(output.write(row[a+9] + "\t" + row[a+10] + "\t" +row[a+11]+"\t" +row[a+12]+"\t" +row[a+13]+"\t"+row[a+14]+"\t" +row[a+17]+"\t" +row[a+18]+"\t" +row[a+19]+"\t" +row[a+20]+"\t" +row[a+21]+"\t"+row[a+22]+"\t" +row[a+24]+"\t" +row[a+25]+"\t" +row[a+26]+"\t"))
                        if len(row)>60:
                                if row[a+50][:9]=='retweeted':
                                        print(output.write(row[a+47]+"\t"+row[a+50] + "\t" + row[a+51] + '\r\n'))
                                elif row[a+49][:9]=='retweeted':
                                        print(output.write(row[a+46]+"\t"+row[a+49] + "\t" + row[a+50] + '\r\n'))
                                else:
                                        print(output.write("\t" +"\t" +'\r\n'))
                        else:
                                print(output.write("\t" +"\t" +'\r\n'))
    # read_tweets_csv('E:/MIT/Fall2k17/Capstone/Twitter_analysis/output27.csv')
    
def clean_tweets(filename):
    from textblob import TextBlob
    import pandas as pd
    tweet_df = pd.read_table(filename,names=('Date','Text','Tweet_id', 'User_Name','Screen_Name',
                                                                        'Location','URL','Description','Followers','Friends','Listed_count','Fav_count',
                                                                        'Statuses_count','Created_date','Time_zone','Geo_enabled','Lang', 'Coordinates',
                                                                        'RT_status','RT_id'))

    tweet_df = cleanTweets(tweet_df)
    # Calculation of sentiments
    polarity = []
    subjectivity = []
    reputation = []
    for i in range(len(tweet_df)):
        wiki = TextBlob(tweet_df['text'][i])
        polarity.append(wiki.sentiment.polarity)
        subjectivity.append(wiki.sentiment.subjectivity)
        try:
            reputation.append(int(tweet_df['Followers'][i].split(':')[1])/(int(tweet_df['Followers'][i].split(':')[1])
            + int(tweet_df['Friends'][i].split(':')[1])))
        except ValueError:
            reputation.append(0)
        except ZeroDivisionError:
            reputation.append(0)
        except IndexError:
            reputation.append(0)
    tweet_df['Polarity'] = polarity
    tweet_df['Subjectivity']= subjectivity
    tweet_df['Reputation'] = reputation
    tweet_df['Reputation'] = round(tweet_df['Reputation'],1)
    return tweet_df

    # tweet_df_passive = clean_tweets('E:/MIT/Fall2k17/Capstone/Twitter_analysis/output27.txt')
    
def cleanTweets(tweet_df):
    import re
    status_row = []
    for i in range(len(tweet_df)):
        status_ = tweet_df.iloc[i,:]['Text'].lower()
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
        list1.append(tweet_df.iloc[i,:]['Location'])
        
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

def plot_sentiments(polarity,subjectivity,reputation):
    import plotly
    import json
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
                title='Scatter'
            )
        )]
    scatter_id = ['Scatter']
    basic_scatter_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return basic_scatter_json,scatter_id



def bar_sentiments(polarity,subjectivity,dates):
    import plotly
    import json
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
                title='Bar',
                barmode='group'
            )
        )]
    bar_id = ['Bar']
    basic_bar_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return basic_bar_json,bar_id

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
            title = 'World Map',
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