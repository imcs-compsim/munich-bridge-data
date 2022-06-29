#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create strain plots for munich-bridge-data publication

Created on Wed Jun 15 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd

import matplotlib.pyplot as plt

import matplotlib.dates as mdates


date = '2022-04-11'

formatter = mdates.DateFormatter('%H:%M')

suffix1 = 'DMS_CNAt' + '100' + 'Hz'
suffix2 = 'ForceAt' + '100' + 'Hz'

titles = ['./Settlements/UniBw_'+date+'_ref_support_load_01',
           # 'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_01',
           # 'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_02',   
           # './Settlements/UniBw_'+date+'_support_load_01',
           # # 'Settlements/Lowering/UniBw_2022-04-11_support_02_lowering',          
           # './Settlements/UniBw_'+date+'_support_load_02',
           # # 'Settlements/Lowering/UniBw_2022-04-11_support_03_lowering',      
           # './Settlements/UniBw_'+date+'_support_load_03'
          ]

fig, ax = plt.subplots()

for i, title in enumerate(titles):

    print('Working on title number: ' + str(i) + '.')
    
    df = pd.read_csv(title + suffix2 + '.csv.zip')
    df['Time (-)'] = pd.to_datetime(df['Time (-)'])
    df.plot(ax = ax, x='Time (-)', y='FRC-01 [kN]', x_compat=True, color='black')
    ax.set_ylabel('FRC-01 [kN]')

    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_minor_formatter(formatter)
    plt.setp( ax.xaxis.get_ticklabels(), rotation=35, ha="right", rotation_mode="anchor") 
    plt.setp( ax.xaxis.get_ticklabels(minor=True), rotation=35, ha="right", rotation_mode="anchor")
    ax.set_xlabel('Time on ' + date)
    
    ax2 = ax.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))

    df2 = pd.read_csv(title + suffix1 + '.csv.zip')  
    df2['Time (-)'] = pd.to_datetime(df2['Time (-)'])
    df2.plot(ax = ax2, x='Time (-)', y='DMS_CN (um/m)', x_compat=True)
    ax2.set_ylabel('DMS_CN [um/m]')


fig.savefig(title + 'StrainsAndForce' + '.pdf', bbox_inches="tight")