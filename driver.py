#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main driver to create plots for munich-bridge-data publication

Created on Wed Jun 15 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd

import Plot as plot

# csv files are in windows encoding
windows = 'cp1252'

# DMS measurements are in the following columns
cols=[0, 11, 16]

# DMS data comes at 1000 Hz. However, 10 values are always constant. Therefore,
# stride = 10
stride = 1000

folder = '/Users/maxvondanwitz/Desktop/'

titles = ['Settlements/UniBw_2022-04-11_ref_support_load_01',
          'Settlements/UniBw_2022-04-11_support_load_01',
          'Settlements/UniBw_2022-04-11_support_load_02',
          'Settlements/UniBw_2022-04-11_support_load_03',
          'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_01',
          'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_02',
          'Settlements/Lowering/UniBw_2022-04-11_support_02_lowering',
          'Settlements/Lowering/UniBw_2022-04-11_support_03_lowering'
          ]

newStarts = []

for i, title in enumerate(titles):

    print('Working on title number: ' + str(i) + '.')
    df = pd.read_csv(folder + title + '.csv', usecols = cols, encoding=windows)  
    df.iloc[:,0] = pd.to_datetime(df.iloc[:,0])
    
    if i == 0:
        mdf = df.iloc[0:-1:stride]
    else:
        newStarts.append(df.iloc[0,0])
        mdf = pd.concat([mdf, df.iloc[0:-1:stride]])

sdf = mdf.sort_values(by=['Time (-)'])
plot.LinesInSubPlotsAndVLines(sdf, x='Time (-)',
                              y = ['DMS_AS (um/m)', 'DMS_CN (um/m)',], newStarts=newStarts,
                              title = title, saveAs='Settlements/UniBw_2022-04-11_complete.pdf')