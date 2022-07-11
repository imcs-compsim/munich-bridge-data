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
cols=[0, 16]

folder = '/Users/maxvondanwitz/Desktop/'

titles = [
          # 'Settlements/UniBw_2022-04-11_ref_support_load_01',
          'Settlements/UniBw_2022-04-11_support_01_ref_ambient',
          # 'Settlements/UniBw_2022-04-11_support_load_01',
          # 'Settlements/UniBw_2022-04-11_support_load_02',
          # 'Settlements/UniBw_2022-04-11_support_load_03',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_01',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_02',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_02_lowering',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_03_lowering'
          ]

for i, title in enumerate(titles):

    print('Working on title number: ' + str(i) + '.')

    df = pd.read_csv(folder + title + '.csv', usecols = cols, encoding=windows)

    mdf = df.iloc[0:-1:10]

    plot.LinesInSubPlots(mdf, x='Time (-)', y = [ 'DMS_CN (um/m)',], title = 'Strains: '+title, saveAs=title+'Strains.pdf')

    # plot.Lines(mdf, x='Time (-)', y = ['FRC-01 [kN]', 'FRC-02 [kN]'], title = 'Force: '+title, ylabel='Force [kN]', saveAs=title+'ForceInline.pdf')