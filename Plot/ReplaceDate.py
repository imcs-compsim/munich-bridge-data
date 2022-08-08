#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strain and force measurement in one plot.

Created on Wed Jun 15 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd

import matplotlib.pyplot as plt

import matplotlib.dates as mdates


date = '2022-03-07'

formatter = mdates.DateFormatter('%H:%M')

suffix1 = 'DMS_CNAt' + '100' + 'Hz'

titles = ['../ReferenceState/ReferenceState',
          ]

fig, ax = plt.subplots()

for i, title in enumerate(titles):

    print('Working on title number: ' + str(i) + '.')

    df = pd.read_csv(title + suffix1 + '.csv.zip')
    df['Time (-)'] = pd.to_datetime(df['Time (-)'])

    for i, ts in enumerate(df.iloc[:,0]):

        df.iloc[i,0] = ts.replace(month = 3, day = 7)

    df.to_csv(title + suffix1 + '.csv.zip', index=False)

