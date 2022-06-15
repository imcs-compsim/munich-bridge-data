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
cols=[0, 18, 19, 20, 21, 22, 48, 49, 50, 51, 52]

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

for title in titles:

    df = pd.read_csv(folder + title + '.csv', usecols = cols, encoding=windows)  

    mdf = df.iloc[0:-1:10]

    plot.LinesInSubPlots(mdf, x='Time (-)', y = ['INC01 (deg)', 'INC02 (deg)',
                                                 'INC03 (deg)', 'INC04 (deg)',
                                                 'INC05 (deg)', 'INC06 (deg)',
                                                 'INC07 (deg)', 'INC08 (deg)',
                                                 'INC09 (deg)', 'INC10 (deg)'], title = 'INC: '+title, saveAs=title+'INC.pdf')