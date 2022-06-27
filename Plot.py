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