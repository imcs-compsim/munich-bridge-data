#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Some ideas on compressing our measured data

Created on Wed Jun 15 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd

import matplotlib.pyplot as plt

import scipy.signal as sig
   
from scipy.ndimage import uniform_filter1d

# Select an example data set
date = '2022-04-11'
suffix1 = 'DMS_CNAt' + '100' + 'Hz'
title = '../Settlements/UniBw_' + date + '_ref_support_load_01'

# Read in and store in data frame
df = pd.read_csv(title + suffix1 + '.csv.zip')  

# For resampling to work (see below), we need our data set as time series.
df['Time on ' + date] = pd.to_datetime(df['Time (-)'])
df = df.set_index('Time on ' + date)
df.drop(['Time (-)'], axis=1, inplace=True)

# 1) The first option is, that we consider is smoothing + brute force downsampling.
## Data smoothing
### Exponentially weighted mean
df['Exponentially weighted mean, span = 100'] = df['DMS_CN (um/m)'].ewm(span=100).mean()
### Uniform filter
df['Uniform filter, window size = 1000'] = uniform_filter1d(df.iloc[:,0].squeeze(), size=int(1000))
title = 'Data smoothing'
df.plot(title=title)
## Brute force downsampling. Picking every 100th data point.
stride = 100
sdf = df.iloc[0:-1:stride].copy()
title = 'Smoothing and picking every 100th data point'
# TODO: Why are the x tick labels different?
fig, ax = plt.subplots()
sdf.plot(ax = ax, title=title)

# 2) Resample
rdf = df.resample('1S').mean()
rdf.plot()


# 3) Use scipy signal decimate to do the job.
sdf['scipy.signal.decimate(factor=100)'] = sig.decimate(df.iloc[:,0].squeeze(), 100, ftype='fir')
sdf.plot()

# TODO: We need some measure to determine which compression techniquie works well.