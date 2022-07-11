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

# Force measurements are in the following columns
cols=[0, 17, 47]

# DMS data comes at 1000 Hz. However, 10 values are always constant. Therefore,
# stride = 10
stride = 10

folder = '/Users/maxvondanwitz/Desktop/'

date = '2022-04-11'

titles = ['Settlements/UniBw_' + date + '_ref_support_load_01',
           'Settlements/UniBw_2022-04-11_support_load_01',
           'Settlements/UniBw_2022-04-11_support_load_02',
           'Settlements/UniBw_2022-04-11_support_load_03',
           'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_01',
           'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_02',
           'Settlements/Lowering/UniBw_2022-04-11_support_02_lowering',
           'Settlements/Lowering/UniBw_2022-04-11_support_03_lowering'
          ]

for title in titles:

    df = pd.read_csv(folder + title + '.csv', usecols = cols, encoding=windows)

    mdf = df.iloc[0:-1:stride].copy()

    mdf['Time (-)'] = pd.to_datetime(mdf['Time (-)'])

    mdf['FRC-01 (N)'] = mdf['FRC-01 (N)'].div(1000)
    mdf['FRC-02 (N)'] = mdf['FRC-02 (N)'].div(1000)
    mdf.rename(columns={'FRC-01 (N)':'FRC-01 [kN]', 'FRC-02 (N)':'FRC-02 [kN]'}, inplace=True)

    plot.Lines(mdf, x='Time (-)', y = ['FRC-01 [kN]', 'FRC-02 [kN]'], title = 'Force: '+title, xlabel='Time on '+date, ylabel='Force [kN]', saveAs=title+'ForceInline.pdf')

    # mdf.to_csv(title + 'ForceAt' + str(1000/stride) + 'Hz.csv.zip', index=False)