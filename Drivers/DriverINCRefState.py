#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main driver to create plots for munich-bridge-data publication

Created on Wed Jun 15 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd

# csv files are in windows encoding
windows = 'cp1252'

# Force measurements are in the following columns
cols=[0, 3, 5]

# DMS data comes at 1000 Hz. However, 10 values are always constant. Therefore,
stride = 10

folder = '../ReferenceState/'

titles = ['Reference State_07032022_FRC_INC',
          ]

for title in titles:

    df = pd.read_csv(folder + title + '.csv', sep='\t', decimal=',', usecols = cols, encoding=windows)

    mdf = df.iloc[0:-1:stride].copy()

    mdf['Time (-)'] = pd.to_datetime(mdf['Time (-)'],yearfirst=True, dayfirst=True)

    mdf.rename(columns={'INC01 (deg)':'INC-01 [deg]', 'INC01 (deg)_Filtered':'INC-01 Filtered [deg]'}, inplace=True)

    mdf.to_csv(title + 'INCAt' + str(1000/stride) + 'Hz.csv.zip', index=False)