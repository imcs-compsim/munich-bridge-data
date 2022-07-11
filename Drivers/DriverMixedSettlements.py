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
cols=[0, 1, 11, 17, 18]

folder = '/Users/maxvondanwitz/Desktop/'

stride = 10

titles = ['Settlements/UniBw_2022-04-11_ref_support_load_01',
          # 'Settlements/UniBw_2022-04-11_support_load_01',
          # 'Settlements/UniBw_2022-04-11_support_load_02',
          # 'Settlements/UniBw_2022-04-11_support_load_03',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_01',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_02',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_02_lowering',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_03_lowering'
          ]

for title in titles:

    df = pd.read_csv(folder + title + '.csv', usecols = cols, encoding=windows)

    mdf = df.iloc[0:-1:stride].copy()

    mdf['Time (-)'] = pd.to_datetime(mdf['Time (-)'])

    mdf.rename(columns={'ACC01_z (g)': 'ACC01_z [g]'}, inplace=True)

    mdf.rename(columns={'DMS_AS (um/m)': 'DMS_AS [um/m]'}, inplace=True)

    mdf['FRC-01 (N)'] = mdf['FRC-01 (N)'].div(1000)
    mdf.rename(columns={'FRC-01 (N)': 'FRC-01 [kN]'}, inplace=True)

    mdf.rename(columns={'INC01 (deg)': 'INC01 [deg]'}, inplace=True)

    plot.LinesInSubPlots(mdf, x='Time (-)',
                         y = ['ACC01_z [g]', 'DMS_AS [um/m]',
                              'FRC-01 [kN]', 'INC01 [deg]'], title = 'AllM: '+title, saveAs=title+'AllM.pdf')

    mdf.to_csv(title + 'AllM' + str(1000/stride) + 'Hz.csv.zip', index=False)