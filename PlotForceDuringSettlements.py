#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot force during settlements for munich-bridge-data publication

Created on Wed Jun 15 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd

import Plot as plot

date = '2022-04-11'

titles = ['./Settlements/UniBw_' + date + '_ref_support_load_01',
          # add,
          # more,
          # files,
          # 
          ]

suffix = 'ForceAt' + '100' + 'Hz'

for title in titles:

    df = pd.read_csv(title + suffix + '.csv')  

    df['Time (-)'] = pd.to_datetime(df['Time (-)'])

    plot.Lines(df, x='Time (-)', y = ['FRC-01 [kN]', 'FRC-02 [kN]'], 
               title = 'Force: '+title, xlabel='Time on '+date, ylabel='Force [kN]',
               saveAs=title + suffix + '.pdf')
