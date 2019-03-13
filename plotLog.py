#! /usr/bin/env python3
import sys
import re
import datetime
import dash
import dash_html_components as html
import dash_core_components as dcc

import dash_table
import pandas as pd

# test db
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

#LOG = ('./data/device_1.log')



def filterLog(string):
   
    try:
        _dateTime = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})') 
        time = _dateTime.search(string).group()
        _state = re.compile(r'(\d$|\d{3}$)')
        state = _state.search(string).group() 

        # conver datetime to datetime object
        t_object = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        return time,state,t_object
    except: 
        #print("no matches")
        pass

    return 

def listAvg(lst):
    return(sum(lst)/len(lst))

def findEdges():
    #t = filterLog(testString) 
    t =[]
    s =[]
    t_obj=[]
    
    with open(LOG) as f:
        for l in f:
            try:
                [_time,_state,_tObj]=filterLog(l)
                t.append(_time)
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
                edge_time.append(t[i])
                state = 0 
         if state == 0:
            if a > 80:
                #print('{}: Move Up'.format(t_obj[i]))
                edge_movement.append('Up')
                edge_time.append(t[i])
                state = 100
    data = {'time': edge_time, 'action': edge_movement}
    df = pd.DataFrame(data)
    return s, t_obj, df 


def main():
    [s,t,df]=findEdges()
    
    return


LOG = sys.argv[1]
df = findEdges()[2]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
html.H1(children='Schedule Testing '),

html.Div(children=''),

    dcc.Graph(
        id='example-graph',

        figure={
            'data': [
                {'x': findEdges()[1], 'y': findEdges()[0], 'type': 'line', 'name': 'curve'}
            ],


            'layout': {
                'title': 'expected vs observed:'

            }
        }
    ),
    # placeholder for data https://dash.plot.ly/datatable see for reference
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),

                    )
])

if __name__ == '__main__':
    print('sorting data for {}'.format(LOG))
    app.run_server(debug=True,host='0.0.0.0', port = 8080)
