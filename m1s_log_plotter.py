import binascii
import datetime
import time
import re
import calendar
import pandas
import logging
import threading
import numpy as np
from matplotlib import pyplot as plt

import cantools
import can

db = cantools.database.load_file('abs.dbc')

# Convert string id to hexadecimal
# 0x18EAF4FA
# strid = '0x18EAF4FA'
# strhex = int(strid,base=16)
# prf = db.decode_message(strhex,message.data)

df = pandas.read_csv('data2.csv')
dfAdjs = df.drop(columns = ['channel'], axis=1)
df_arr = dfAdjs.to_numpy()

dim = df_arr.shape
baris = dim[0]
kolom = dim[1]

# table id=353, data 4, row length equal to all data
whs = np.empty([2, 5], dtype=float) #1 time stamp + 4 data

dataCanArray = np.empty([baris, 11],dtype=int) # Kolom contain timestamp,ID,DLC and 8byte data |timestamp|DLC|Data0 .... Data7|

# index input data correspondent to ID
iter1 = 0

for n in range(baris):
    dataCanArray[n][0] = float(df_arr[n][0])
    dataCanArray[n][1] = int(df_arr[n][1],base=16)  # if no information about DLC int(8) # if no information about DLC
    dataCanArray[n][2] = int(8)
    for m in range(3,11,1):
        try:
            dataCanArray[n][m] = int(df_arr[n][m-1], base=16)
        except:
            dataCanArray[n][m] = int(df_arr[n][m-1])

    arrByte = bytearray(8)
    for i in range(3,11,1):
        arrByte[i-3] = dataCanArray[n][i]

    Id = int(dataCanArray[n][1])
    prf = db.decode_message(Id, arrByte)

    # index row for i is whs
    if Id == 835:
        whs[iter1, 0] = dataCanArray[n][0]
        whs[iter1, 1] = prf["whlspeed_FL"]
        whs[iter1, 2] = prf["whlspeed_FR"]
        whs[iter1, 3] = prf["whlspeed_RL"]
        whs[iter1, 4] = prf["whlspeed_RR"]
        iter1 = iter1+1

    print(prf)


plt.title("Wheels Speed Vs Time")
plt.xlabel("Time")
plt.ylabel("Wheel Speed (kmh)")
plt.plot(whs[:,0],whs[:,1])
plt.show()

loop = True
while(loop):
    time.sleep(1)

# ======================================================================================================================

predf = df.drop(columns = ['CAN_CHNL','CAN(FD)','BRS','Type'], axis=1)
nrows = len(predf.index)

nrowImp = 0

startTime = time.time()
print('Start time :' + str(startTime) )

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

    xdata=[]*8
    xdatab=[]*8

    if predf.loc[x,['DLC']].values[0] < 8:
        iter = int(predf.loc[x,['DLC']].values[0])
    else:
        iter = 8

    for i in range(3,iter+3):
        temp = (predf.iat[x,i]).encode('utf-8')
        xdata.append(temp)

    # xdatab = bytearray(xdata)

    # consolid = "b'" + xdata0 + xdata1 + xdata2 + xdata3 + xdata4 + xdata5 + xdata6 + xdata7 + "\'"
    # print(consolid)

    #print(str_epoc)
    nrowImp = nrowImp + 1
    
print('done')
    
finishTime = time.time()
print('Finish time :' + str(finishTime) )

executionTime = finishTime - startTime
print('Execution time : ' + str(executionTime))
