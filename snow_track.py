#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 15:24:52 2018

@author: isaactrussell
"""

import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from numpy import *
plt.style.use('ggplot')

def snow_scrape():
    output = os.getcwd() + "/data.csv"
#       7 Day Data
#    raw = pd.read_html('https://wcc.sc.egov.usda.gov/reportGenerator/view/customSingleStationReport/daily/978:id:SNTL/-7,0/WTEQ::value,SNWD::value,PREC::value,TOBS::value,TMAX::value,TMIN::value,TAVG::value')[38]
#       30 Day Data 
    raw = pd.read_html('https://wcc.sc.egov.usda.gov/reportGenerator/view/customSingleStationReport/daily/start_of_period/978:ID:SNTL%7Cid=%22%22%7Cname/-29,0/WTEQ::value,SNWD::value,PREC::value,TOBS::value,TMAX::value,TMIN::value,TAVG::value?fitToScreen=false')[38]
    raw.set_index("Date", inplace = True)
    raw.columns = ['Snow Water Eq', 'Snow Depth', 'Precip', 'Temp Start', 'Temp Max', 'Temp Min', 'Temp Avg']
    raw.dropna(how = 'any', inplace = True)
    if os.path.exists(output):
        existing = pd.read_csv(output).set_index('Date')
        for date in raw.index:
            if date in existing.index:
                raw.drop(date, inplace = True)
        if raw.shape[0] == 0:
            print('no new data added')
        else:
            with open(output, 'a') as f:
                raw.to_csv(output, mode = 'a', header = False)
            print('{} records added!'.format(raw.shape[0]))
    else:
        print('New File')
        raw.to_csv(output)

data_path = os.getcwd() + '/data.csv'
if os.path.exists(data_path):
    access = datetime.datetime.fromtimestamp(os.stat(data_path).st_mtime)
    delta = datetime.datetime.now() - access
    if delta.days < 1:
        data = pd.read_csv(data_path).set_index('Date')
        print("Reading old data")
    else:
        snow_scrape()
#        print('Appending new data')
        data = pd.read_csv(data_path).set_index('Date')
else:
    snow_scrape()
    print('Creating new file')
    data = pd.read_csv(data_path)

    
freeze = array([32 for _ in range(data['Temp Avg'].shape[0])])
fig, axes = plt.subplots(nrows=2, ncols=1, sharex = True, figsize = (13, 6.9))
fig.suptitle('Bogus Basin 2018-2019 Season Conditions', fontsize = 13)
axes[0].set_ylabel('Deg F')
axes[1].set_ylabel('in')
axes[0].axhline(y = 32, color = 'b', linestyle = ':')
data.plot(x = data.index, y = ['Temp Avg'], ax = axes[0], title = "Temperature", color = 'k')
data.plot(x = data.index, y = ['Snow Depth'], ax = axes[1], title = "Snow")