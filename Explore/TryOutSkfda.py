#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main driver to create plots for munich-bridge-data publication

Created on Wed Jul 13 07:47:59 2022

@author: maxvondanwitz
"""

import pandas as pd

import skfda

import skfda.preprocessing.smoothing.kernel_smoothers as ks

import scipy.signal as sig

# Select an example data set
date = '2022-04-11'
suffix1 = 'DMS_CNAt' + '100' + 'Hz'
title = '../Settlements/UniBw_' + date + '_ref_support_load_01'

# Read in and store in data frame
df = pd.read_csv(title + suffix1 + '.csv.zip')

# For the functional data analysis of Skfda to work, we convert our data frame
# to an FDataGrid.
data_matrix = df.iloc[:,1].to_numpy()
grid_points = df.index.to_numpy()
fd = skfda.FDataGrid(
                        data_matrix=data_matrix,
                        grid_points=grid_points
                      )
# Just like data frames, FDataGrid has a convenient plotting function.
fd.plot()

# Let's try to represent the data on a spline basis.
splineBasis = skfda.representation.basis.BSpline(
        n_basis=200,
        domain_range=fd.domain_range,
    )
fd_on_Basis = fd.to_basis(splineBasis)

# Looks ok.
fd_on_Basis.plot()

# And on a Fourier basis, ...
fourierBasis = skfda.representation.basis.Fourier(
        # n_basis=720,
        n_basis=100,
        domain_range=fd.domain_range,
    )

fd_on_Basis = fd.to_basis(fourierBasis)
# ... which is a little wiggely for 100 basis functions.
fd_on_Basis.plot()

# There are more sophisticated smoothers in skfda, but they are slow, so let's
# pick a smaller data set.
## 1. Brute force downsampling. Picking every 100th data point.
stride = 100
sdf = df.iloc[0:-1:stride].copy()
## 2. Decimate
sdf['scipy.signal.decimate(factor=100)'] = sig.decimate(df.iloc[:,1].squeeze(), 100, ftype='fir')
sdf.plot()

# Our small functional data set.
data_matrix = sdf.iloc[:,2].to_numpy()
grid_points = sdf.index.to_numpy()

sfd = skfda.FDataGrid(
                        data_matrix=data_matrix,
                        grid_points=grid_points
                      )

sfd.plot()

# KNeighborsSmoother is quite agressive.
smoother = ks.KNeighborsSmoother(smoothing_parameter = 10)
sfd_smooth = smoother.fit_transform(sfd)
sfd_smooth.plot()

# LocalLinearRegressionSmoother get rid of some high frequency noise,
# looks actually pretty good.
smoother = ks.LocalLinearRegressionSmoother(smoothing_parameter = 250)
sfd_smooth = smoother.fit_transform(sfd)
sfd_smooth.plot()

# NadarayaWatsonSmoother is somewhere in between...
smoother = ks.NadarayaWatsonSmoother(smoothing_parameter = 100)
sfd_smooth = smoother.fit_transform(sfd)
sfd_smooth.plot()
