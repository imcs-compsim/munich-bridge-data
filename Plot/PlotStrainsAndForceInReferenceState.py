#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strain and force measurement in one plot.

Created on Wed Jun 15 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd

import matplotlib.pyplot as plt

import matplotlib.dates as mdates

from matplotlib.ticker import MaxNLocator

date = '2022-03-07'

formatter = mdates.DateFormatter('%H:%M')

suffix1 = 'DMS_CNAt' + '100' + 'Hz'
suffix2 = 'ForceAt' + '100' + 'Hz'

titles = ['../ReferenceState/ReferenceState',
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


    linestyles = ["-", "--"]
    df = pd.read_csv(title + suffix2 + '.csv.zip')
    df['Time (-)'] = pd.to_datetime(df['Time (-)'])
    # df.plot(ax = ax, x='Time (-)', y=['FRC-01 (kN)','FRC-02 (kN)'], x_compat=True, color='black', alpha=0.5)
    df.plot(ax = ax, x='Time (-)', y=['FRC-01 (kN)','FRC-02 (kN)'], color =['black', 'black'], style = linestyles, x_compat=True)
    ax.set_ylabel('FRC-01/2 [kN]')

    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_minor_formatter(formatter)
    plt.setp( ax.xaxis.get_ticklabels(), rotation=35, ha="right", rotation_mode="anchor")
    plt.setp( ax.xaxis.get_ticklabels(minor=True), rotation=35, ha="right", rotation_mode="anchor")
    ax.set_xlabel('Time on ' + date)
    ax.legend(['FRC-01', 'FRC-02'])
    ax.xaxis.set_major_locator(MaxNLocator(7))

    ax2 = ax.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))

    df2 = pd.read_csv(title + suffix1 + '.csv.zip')
    df2['Time (-)'] = pd.to_datetime(df2['Time (-)'])
    df2.plot(ax = ax2, x='Time (-)', y='DMS_CN (um\m)', x_compat=True, color = 'grey')
    ax2.set_ylabel('DMS-CN [um/m]')
    ax2.legend(['DMS-CN'])

    # ask matplotlib for the plotted objects and their labels
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, ['FRC-01', 'FRC-02','DMS-CN'], ncol=3, loc='upper center', bbox_to_anchor=(0.5, 1.27))
    # ax2.legend(lines + lines2, labels + labels2)
    ax.get_legend().remove()


fig.savefig(title + 'StrainsAndForce' + '.pdf', bbox_inches="tight")