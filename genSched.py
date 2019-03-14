import sys
import re
from datetime import date, datetime, timedelta
import dash
import dash_html_components as html
import dash_core_components as dcc

import dash_table
import pandas as pd

# test db
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

LOG = ('./data/device_2.log')

# predefined schedule
SCHED = {'8:00':'Lower','10:30':'Raise',
        '10:35':'Lower','12:30':'Raise',
        '12:35':'Lower','13:30':'Raise',
        '13:35':'Lower','14:30':'Raise',
        '14:35':'Lower','16:30':'Raise',
        '16:35':'Lower','19:30':'Raise',
        '19:35':'Lower','10:00':'Raise'}


def filterLog(string):

    try:
        _dateTime = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
        time = _dateTime.search(string).group()
        _state = re.compile(r'(\d$|\d{3}$)')
        state = _state.search(string).group()

        # conver datetime to datetime object
        t_object = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        return time,state,t_object
    except:
        #print("no matches")
        pass

    return

def listAvg(lst):
    return(sum(lst)/len(lst))


# generator function for creating schedule accross time-span
def daterange(start_date,end_date):
    for n in range(int((end_date-start_date).days)):
        yield start_date + timedelta(n)

def generateSchedule(listofDateTime):
    span = [min(listofDateTime),max(listofDateTime)]
    print(span)
    t = []
    s = []
    # format the schedules to time
    for key in SCHED:
        t.append(key)
        s.append(SCHED[key])
    t = [datetime.strptime(i,'%H:%M').time() for i in t]
    print(daterange(span[0],span[1]))
    d = {}
    for single_date in daterange(span[0],span[1]+timedelta(days=1)):
        d[single_date.date()] = [t,s]

    return d

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
    return t_obj, df


def main():
    [t,df]=findEdges()
    return

if __name__ == '__main__':

    [t,df] = findEdges()
    d = generateSchedule(t)

    print(d)
    

