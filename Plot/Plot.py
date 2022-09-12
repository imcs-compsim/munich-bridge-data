#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 07:54:01 2022

@author: maxvondanwitz
"""
import matplotlib.pyplot as plt

def Points(df, x, y, saveAs=''):

    fig, ax = plt.subplots()

    ax = df.plot(x=x, y=y, kind='scatter',xticks = [])

    ax.set_xlabel('Date and Time')

    if len(y) == 1:
        ax.set_ylabel(y[0])
        # ax.get_legend().remove()

    # plt.setp( ax.xaxis.get_majorticklabels(), rotation=35, ha="right", rotation_mode="anchor")

    fig = ax.get_figure()

    if saveAs == '':
        fig.show()
    else:
        fig.savefig(saveAs,bbox_inches="tight")

    plt.show()


def Lines(df, x, y, title, xlabel, ylabel ='', saveAs=''):

    fig, ax = plt.subplots()

    ax = df.plot(x=x, y=y, subplots=False, title=title)

    if xlabel != '':
        ax.set_xlabel(xlabel)

    if ylabel != '':
        ax.set_ylabel(ylabel)

    if len(y) == 1:
        ax.set_ylabel(y[0])
        ax.get_legend().remove()

    plt.setp( ax.xaxis.get_majorticklabels(), rotation=35, ha="right", rotation_mode="anchor")
    plt.setp( ax.xaxis.get_ticklabels(minor=True), rotation=35, ha="right", rotation_mode="anchor")

    fig = ax.get_figure()

    if saveAs == '':
        fig.show()
    else:
        fig.savefig(saveAs,bbox_inches="tight")

    plt.show()

def LinesBW(df, x, y, title, xlabel, ylabel ='', saveAs=''):

    import matplotlib.dates as mdates

    from matplotlib.ticker import MaxNLocator

    formatter = mdates.DateFormatter('%H:%M')

    cm = 1/2.54

    plt.rcParams['font.sans-serif'] = "Arial"
    plt.rcParams.update({'font.size': 8})

    plt.rcParams['figure.figsize'] =  (5.5*cm, 3.8*cm)


    linestyles = ["-", "-"]
    colors = ['black', 'grey']

    fig, ax = plt.subplots()

    ax = df.plot(x=x, y=y, subplots=False, color = colors , style=linestyles, x_compat=True)

    if xlabel != '':
        ax.set_xlabel(xlabel)

    if ylabel != '':
        ax.set_ylabel(ylabel)

    if len(y) == 1:
        ax.set_ylabel(y[0])
        ax.get_legend().remove()

    plt.setp( ax.xaxis.get_majorticklabels(), rotation=35, ha="right", rotation_mode="anchor")
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_locator(MaxNLocator(7))

    fig = ax.get_figure()

    if saveAs == '':
        fig.show()
    else:
        fig.savefig(saveAs,bbox_inches="tight")

    plt.show()

def LinesInSubPlots(df, x, y, title, saveAs=''):

    fig, ax = plt.subplots()

    axArr = df.plot(x=x, y=y, subplots=True, title = title)

    for i, ax in enumerate(axArr):
        ax.set_xlabel('Date and Time')
        ax.set_ylabel(y[i], rotation = 'horizontal')
        ax.yaxis.set_label_coords(-0.25,0.5)
        ax.get_legend().remove()
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=35, ha="right", rotation_mode="anchor")

    fig = axArr[0].get_figure()

    if saveAs == '':
        fig.show()
    else:
        fig.savefig(saveAs,bbox_inches="tight")

    plt.show()

def LinesInSubPlotsOn(date, df, x, y, title, saveAs=''):

    fig, ax = plt.subplots()

    axArr = df.plot(x=x, y=y, subplots=True, title = title)

    for i, ax in enumerate(axArr):
        ax.set_xlabel('Time on ' + date)
        ax.set_ylabel(y[i], rotation = 'horizontal')
        ax.yaxis.set_label_coords(-0.25,0.5)
        ax.get_legend().remove()
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=35, ha="right", rotation_mode="anchor")

    fig = axArr[0].get_figure()

    if saveAs == '':
        fig.show()
    else:
        fig.savefig(saveAs,bbox_inches="tight")

    plt.show()

def LinesInSubPlotsAndVLines(df, x, y, newStarts, title, saveAs=''):

    fig, ax = plt.subplots()

    axArr = df.plot(x=x, y=y, subplots=True, title = title)

    for i, ax in enumerate(axArr):

        for newStart in newStarts:
            ax.axvline(newStart, color='k')

        ax.set_xlabel('Date and Time')
        ax.set_ylabel(y[i], rotation = 'horizontal')
        ax.yaxis.set_label_coords(-0.25,0.5)
        ax.get_legend().remove()
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=35, ha="right", rotation_mode="anchor")

    fig = axArr[0].get_figure()

    if saveAs == '':
        fig.show()
    else:
        fig.savefig(saveAs,bbox_inches="tight")

    plt.show()