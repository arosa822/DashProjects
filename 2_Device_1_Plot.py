#! /usr/bin/env python3
import sys
import re
import datetime
from datetime import date, timedelta
import dash
import dash_html_components as html
import dash_core_components as dcc

import dash_table
import pandas as pd

# test db
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

LOG1 = ('./data/device_1.log')
LOG2 = ('./data/device_2.log')

#LOG=sys.argv[1] 

# predefined schedule
SCHED = {'8:00':0,'11:30':100,
        '11:35':0,'13:30':100,
        '13:35':0,'14:30':100,
        '14:35':0,'15:30':100,
        '15:35':0,'18:30':100,
        '18:35':0,'19:30':100,
        '19:35':0,'22:00':100}


# generator for grabbing the days within timespan of log
def daterange(start_date,end_date):
        for n in range(int((end_date-start_date).days)):
                    yield start_date + timedelta(n)

# depending on the span of time create a schedule based on the data above
def generateSchedule(listofDateTime):
    span = [min(listofDateTime),max(listofDateTime)]
    t=[]
    s=[]
    # format the schedules to time
    for key in SCHED:
        t.append(key)
        s.append(SCHED[key])
    #t=[datetime.strptime(i,'%H:%M').time() for i in t]

    d = {}
    for single_date in daterange(span[0],span[1]+timedelta(days=1)):
        d[single_date] = [t,s]

    return d

def expandToList(dictionary):
    '''This module expands the dictionary of schedules into a list, dates need to be duplicated to fill t
    '''
    _date = []
    _time = []
    _state =[]
    for k in dictionary:
        for i in dictionary[k][0]:
            _time.append(i)
        for i in dictionary[k][1]:
            _state.append(i)
        for i in range(0,len(dictionary[k][1])):
            _date.append(k)
    #HACK: combine datetime and day
    n = 0
    updatedDate = []
    updatedState = []

    for i in _date:
        _date[n] = datetime.datetime.combine(_date[n].date(),datetime.datetime.strptime(_time[n],'%H:%M').time())

        if n == 0:
            updatedState.append(_state[n])
            updatedDate.append(_date[n])
        else:
            updatedState.append(_state[n-1])
            updatedState.append(_state[n])
            updatedDate.append(_date[n]-timedelta(seconds=1))
            updatedDate.append(_date[n])

        n += 1
    
    df=pd.DataFrame({'Datetime':updatedDate,'Action':updatedState})
    return df

def filterLog(string):
   
    try:
        _dateTime = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})') 
        time = _dateTime.search(string).group()
        _state = re.compile(r'(\d$|\d{3}$)')
        state = _state.search(string).group() 

        # conver datetime to datetime object
        t_object = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        return state,t_object
    except: 
        #print("no matches")
        pass

    return 

def listAvg(lst):
    return(sum(lst)/len(lst))

def findEdges(LogFile):
    #t = filterLog(testString) 
    t =[]
    s =[]
    t_obj=[]
    
    with open(LogFile) as f:
        for l in f:
            try:
                [_state,_tObj]=filterLog(l)
                s.append(int(_state))
                t_obj.append(_tObj)
                edge_movement=[]
                edge_time = []
            except TypeError: 
                pass
    movingAvg = 5 
    if listAvg(s[:5]) == 0:
        state = 0
    else:
        state = 100


    for i in range(0,len(s)-movingAvg):
         a = listAvg(s[i:i+movingAvg])
         if state == 100:
             if a < 40:
                #print('{}: Move Down'.format(t_obj[i]))
                edge_movement.append('Down')
                edge_time.append(t_obj[i])
                state = 0 
         if state == 0:
            if a > 80:
                #print('{}: Move Up'.format(t_obj[i]))
                edge_movement.append('Up')
                edge_time.append(t_obj[i])
                state = 100
    data = {'time': edge_time, 'action': edge_movement}
    #df = pd.DataFrame(data)
    observed =pd.DataFrame({'time':t_obj,'state':s})
 
    return observed#, df 


def main():
    obs_1=findEdges(LOG1)
    

    obs_2=findEdges(LOG2)
    

    schedule = generateSchedule(obs_2['time'])

    d = expandToList(schedule)
    #print(d['Datetime'])
    
    print('First set:')
    n = 0 
    while n< 5:
        print(obs_1['time'][n])
        n += 1
    print('Second set:')
    n = 0 
    while n< 5:
        print(d['Datetime'][n])
        n += 1
    print(type(obs_1['time'][0]))
    print(type(d['Datetime'][0]))

    return

obs_1=findEdges(LOG1)


obs_2=findEdges(LOG2)


schedule = generateSchedule(obs_2['time'])

d = expandToList(schedule)
#
#[s_1,t_obj_1,df_1]=findEdges(LOG1)
#
#[s_2,t_obj_2,df_2]=findEdges(LOG2)
#
#print('sorting data for {}'.format(LOG1))
#print(len(t_obj_1),len(s_1))
#schedule = generateSchedule(t_obj_1)
#
#d = expandToList(schedule)
##########################################################################
# start of dash visualizations
##########################################################################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
html.H1(children='Data Vizzzz..  '),

html.Div(children=''),

    dcc.Graph(
        id='example-graph',

        figure={
            'data': [
                {'x': obs_2['time'], 'y': obs_2['state'], 'type': 'line', 'name': LOG1},
                {'x': d['Datetime'], 'y': d['Action'], 'type': 'line', 'name':'Expected'}

            ],


            'layout': {
                'title': 'simulated + ' + LOG1

            }
        }
    )
    # placeholder for data https://dash.plot.ly/datatable see for reference
   # dash_table.DataTable(
   #     id='table',
   #     columns=[{"name": i, "id": i} for i in df_1.columns],
   #     data=df_1.to_dict("rows"),

   #                 )
])

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0', port = 8080)
    #main()
