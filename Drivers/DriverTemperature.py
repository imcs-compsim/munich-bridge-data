#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot temperature during reference measurement for munich-bridge-data publication

Created on Wed Jun 29 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd

import Plot as plot

titles = ['./Weather/TemperatureComparisonMUC',
          # add,
          # more,
          # files,
          # 
          ]

for title in titles:

    df = pd.read_csv(title + '.csv', delimiter=';', decimal=',')

    df['day'] = pd.to_datetime(df['day'])

    plot.Lines(df, x='day', y = ['TMinFH', 'TMinB', 'TMaxFH', 'TMaxB'], 
               title = title, 
               xlabel='Date',
               ylabel='Temperature [deg. C]',
               saveAs=title + '.pdf')

    df.to_csv(title + '.csv', index=False)