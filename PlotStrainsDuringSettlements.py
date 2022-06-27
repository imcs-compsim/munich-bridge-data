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

suffix = 'DMS_CNAt' + '100' + 'Hz'

titles = ['./Settlements/UniBw_'+date+'_ref_support_load_01',
           # 'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_01',
           # 'Settlements/Lowering/UniBw_2022-04-11_support_01_lowering_02',   
           './Settlements/UniBw_'+date+'_support_load_01',
           # 'Settlements/Lowering/UniBw_2022-04-11_support_02_lowering',          
           './Settlements/UniBw_'+date+'_support_load_02',
           # 'Settlements/Lowering/UniBw_2022-04-11_support_03_lowering',      
           './Settlements/UniBw_'+date+'_support_load_03'
          ]

fig, ax = plt.subplots(nrows=1, ncols=4, sharey='all')

for i, title in enumerate(titles):

    print('Working on title number: ' + str(i) + '.')
    df = pd.read_csv(title + suffix + '.csv.zip')
    
    df['Time (-)'] = pd.to_datetime(df['Time (-)'])
    
    curAx = ax.flat[i]
    df.plot(ax = curAx, x='Time (-)', y='DMS_CN (um/m)', x_compat=True)

    curAx.get_legend().remove()

    curAx.set_xlabel(' ')    
    curAx.xaxis.set_label_coords(-0.1, -0.25)
    curAx.xaxis.set_major_formatter(formatter)
    plt.setp( curAx.xaxis.get_ticklabels(), rotation=35, ha="right", rotation_mode="anchor") 


ax.flat[2].set_xlabel('Time on ' + date)

ax.flat[0].set_ylabel('DMS_CN [um/m]')
ax.flat[0].yaxis.set_label_coords(-0.5, 0.5)

fig.savefig(title + suffix + '.pdf', bbox_inches="tight")