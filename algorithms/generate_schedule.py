#! /usr/bin/env python3
import sys
from datetime import date, datetime, timedelta
import random


'''
Date Created: 3/13
Author: Alex Rosa 

Description
Method for generating a list of schedules spaning a specified time,
given a table of occurances during the day (hour / minute).

'''
# test times (generate random date between 3/10 and 3/30)
START_END = ['3/' + str(random.randint(10,19)) + ' 08:20',
            '3/' + str(random.randint(20,30)) + ' 16:25']

# predefined schedule
SCHED = {'8:00':'Lower','10:30':'Raise',
        '10:35':'Lower','12:30':'Raise',
        '12:35':'Lower','13:30':'Raise',
        '13:35':'Lower','14:30':'Raise',
        '14:35':'Lower','16:30':'Raise',
        '16:35':'Lower','19:30':'Raise',
        '19:35':'Lower','10:00':'Raise'}


# convert string to datetime object
# could do this first, but i included this step for reference
DATE_OBJ=[datetime.strptime(i,'%m/%d %H:%M') for i in START_END]


# generator for grabbing the days within timespan of log
def daterange(start_date,end_date):
    for n in range(int((end_date-start_date).days)):
        yield start_date + timedelta(n)


# generate random time sequence of dates between the two dates specified above
def generateData(start, end, delta):
    '''
    fills in list of random data between the two dates within START_END
    :PARAM start: 
    :PARAM end: 
    :PARAM delta: 
    '''
    curr = start
    listofDateTime = []
    while curr < end: 
        listofDateTime.append(curr.date())
        curr += delta
    return listofDateTime


# depending on the span of time create a schedule based on the data above
def generateSchedule(listofDateTime):
    span = [min(listofDateTime),max(listofDateTime)]
    t=[]
    s=[]
    # format the schedules to time     
    for key in SCHED:
        t.append(key)
        s.append(SCHED[key])
    t=[datetime.strptime(i,'%H:%M').time() for i in t]

    d = {}    
    for single_date in daterange(span[0],span[1]+timedelta(days=1)):
        d[single_date] = [t,s]
   
    return d


def main():
    testData = generateData(DATE_OBJ[0],DATE_OBJ[1], timedelta(minutes = random.randint(15,40))) 
    schedule = generateSchedule(testData)
    return print(schedule)

if __name__ == '__main__':
    sys.exit(main())

