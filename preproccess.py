# -*- coding: utf-8 -*-

import datetime
import time
import re
import calendar
#import csv
import pandas
 
df = pandas.read_csv('CH0_Bike_logger0.csv')
predf = df.drop(columns = ['CAN_CHNL','CAN(FD)','BRS','Type','DLC'], axis=1)
nrows = len(predf.index)

nrowImp = 0

startTime = time.time()
print('Start time :' + str(startTime) )

# grep date data
# strTime = predf.loc[:,['Time']]
# strTimeRow1 = df.loc[0,['Time']].values[0]

for x in range(nrows):
    strTimeRow1 = predf.loc[x,['Time']].values[0]
    strSp = re.split(r'-|_|:',strTimeRow1)

    seconds = float(strSp[5])
    secondsInt = int(seconds)
    minutes = int(strSp[4])
    hours = int(strSp[3])
    day = int(strSp[2])
    month = int(strSp[1])
    year = int(strSp[0])
        
    t=datetime.datetime(year, month, day, hours, minutes, secondsInt)
    f_epoc = float(calendar.timegm(t.timetuple())) + (seconds - float(secondsInt))
    str_epoc = str(f_epoc)
    predf.loc[x,['Time']] = str_epoc
    #print(str_epoc)
    nrowImp = nrowImp + 1
    
print('done')
    
finishTime = time.time()
print('Finish time :' + str(finishTime) )

executionTime = finishTime - startTime
print('Execution time : ' + str(executionTime))
    
# strDate = "2023-05-21_08:43:48.212"

# strSp = re.split(r'-|_|:',strDate)

# seconds = float(strSp[5])
# secondsInt = int(seconds)
# minutes = int(strSp[4])
# hours = int(strSp[3])
# day = int(strSp[2])
# month = int(strSp[1])
# year = int(strSp[0])

# # strTime = seconds + minutes*60 + hours*3600 + day*86400 + (year-70)*31536000 + ((year-69)/4)*86400 - ((year-1)/100)*86400 + ((year+299)/400)*86400


# t=datetime.datetime(year, month, day, hours, minutes, secondsInt)
# f_epoc = float(calendar.timegm(t.timetuple())) + (seconds - float(secondsInt))
# str_epoc = str(f_epoc)
# print(str_epoc)
