#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main driver to create plots for munich-bridge-data publication

Created on Wed Jun 15 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd

import Plot as plot

date = '2022-04-11'

titles = ['./Settlements/UniBw_2022-04-11_ref_support_load_01',
          # 'Settlements/UniBw_2022-04-11_support_load_01',
          # 'Settlements/UniBw_2022-04-11_support_load_02',
          # 'Settlements/UniBw_2022-04-11_support_load_03',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_01',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_02',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_02_lowering',
          # 'Settlements/Lowering/UniBw_2022-04-11_support_03_lowering'
          ]

for title in titles:

    df = pd.read_csv( title + 'AllM100Hz.csv.zip')  

    
    df['Time (-)'] = pd.to_datetime(df['Time (-)'])
    

    plot.LinesInSubPlotsOn(date, df, x='Time (-)',
                         y = ['ACC01_z [g]', 'DMS_AS [um/m]',
                              'FRC-01 [kN]', 'INC01 [deg]'], title = 'AllM: '+title, saveAs=title+'AllM.pdf')
    