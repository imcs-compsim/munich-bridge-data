#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot temperature during reference measurement for munich-bridge-data publication

Created on Wed Jun 29 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd
import matplotlib.pyplot as plt

def LinesBW(df, x, y, title, xlabel, ylabel ='', saveAs=''):

    import matplotlib.dates as mdates

    from matplotlib.ticker import MaxNLocator

    formatter = mdates.DateFormatter('%d')

    cm = 1/2.54
    plt.rcParams['figure.figsize'] =  (5.5*cm, 3.8*cm)

    plt.rcParams['font.sans-serif'] = "Arial"
    plt.rcParams.update({'font.size': 8})

    colors = ['black', 'black' ,'grey', 'grey']
    linestyles = ["--", "-", "--", "-"]

    fig, ax = plt.subplots()

    ax = df.plot(x=x, y=y, subplots=False, color = colors, style=linestyles, x_compat=True)


    if xlabel != '':
        ax.set_xlabel(xlabel)

    if ylabel != '':
        ax.set_ylabel(ylabel)

    if len(y) == 1:
        ax.set_ylabel(y[0])
        ax.get_legend().remove()

    plt.setp( ax.xaxis.get_majorticklabels(), rotation=35, ha="right", rotation_mode="anchor")

    ax.legend(['Tmin Airport Munich', 'Tmin Test Bridge', 'Tmax Airport Munich', 'Tmax Test Bridge'], bbox_to_anchor=(1.05, 0.85))

    ax.xaxis.set_major_locator(MaxNLocator(10))
    ax.xaxis.set_major_formatter(formatter)

    fig = ax.get_figure()

    if saveAs == '':
        fig.show()
    else:
        fig.savefig(saveAs,bbox_inches="tight")

    plt.show()

titles = ['../Weather/TemperatureComparisonMUC',
          # add,
          # more,
          # files,
          #
          ]

for title in titles:

    df = pd.read_csv(title + '.csv')

    df['day'] = pd.to_datetime(df['day'])

    LinesBW(df, x='day', y = ['TMinFH', 'TMinB', 'TMaxFH', 'TMaxB'],
               title = title,
               xlabel='Date in March 2022',
               ylabel='Temperature [deg. C]',
               saveAs=title + '.pdf')


