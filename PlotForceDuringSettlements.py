#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot force during settlements for munich-bridge-data publication

Created on Wed Jun 15 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd

import Plot as plot

titles = ['./Settlements/UniBw_2022-04-11_ref_support_load_01',
          # add,
          # more,
          # files,
          # 
          ]

suffix = 'ForceAt' + '100' + 'Hz'

for title in titles:

    df = pd.read_csv(title + suffix + '.csv')  

    plot.Lines(df, x='Time (-)', y = ['FRC-01 [kN]', 'FRC-02 [kN]'], 
               title = 'Force: '+title, ylabel='Force [kN]',
               saveAs=title + suffix + '.pdf')
