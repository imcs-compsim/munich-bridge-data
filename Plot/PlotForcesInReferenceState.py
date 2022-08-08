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


date = '2022-03-07'

formatter = mdates.DateFormatter('%H:%M')

suffix1 = 'ForceAt' + '100' + 'Hz'

titles = ['../ReferenceState/ReferenceState',
          ]

fig, ax = plt.subplots()

for i, title in enumerate(titles):

    print('Working on title number: ' + str(i) + '.')

    df = pd.read_csv(title + suffix1 + '.csv.zip')
    df['Time (-)'] = pd.to_datetime(df['Time (-)'])
    df.plot(ax = ax, x='Time (-)', y=['FRC-01 (kN)','FRC-02 (kN)'], x_compat=True)
    ax.set_ylabel('FRC-01/2 [kN]')

    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_minor_formatter(formatter)
    plt.setp( ax.xaxis.get_ticklabels(), rotation=35, ha="right", rotation_mode="anchor")
    plt.setp( ax.xaxis.get_ticklabels(minor=True), rotation=35, ha="right", rotation_mode="anchor")
    ax.set_xlabel('Time on ' + date)

fig.savefig(title + 'Force' + '.pdf', bbox_inches="tight")