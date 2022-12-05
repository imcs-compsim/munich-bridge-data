#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 14:06:29 2022

@author: maxvondanwitz
"""

# Minimal FFT usage example inspired by the following page
# https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.04-FFT-in-Python.html

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft
import pandas as pd

# Select an example data set
date = '2022-04-11'
suffix = 'AllM' + '100' + 'Hz'
title = '../Settlements/UniBw_' + date + '_ref_support_load_01'

# Read in and select the data of acceleration sensor #1
df = pd.read_csv(title + suffix + '.csv.zip')
signal = df['ACC01_z [g]'].to_numpy()

# What do we know about our signal?
# We have 72000 data points.
N = len(signal)
# As the suffix of the loaded file suggests, the sampling rate is 100 Hz  
sr = 100.0
# So, the measurement must have taken 12 minutes = 72000 seconds.
T = N/sr
# Relative to t_0 = 0, we reconstruct the measurement time instances.
t = np.arange(0, T, 1.0/sr)

plt.figure(figsize = (12, 6))
plt.subplot(121)

# Let's draw the signal.
plt.plot(t, signal, 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

# Compute FFT
Xk = fft(signal)

# The discrete Fourier transform produces equally-spaced samples of the 
# discrete-time Fourier transform (DTFT). The interval at which the DTFT is 
# sampled is the reciprocal of the duration of the input sequence.
# https://en.wikipedia.org/wiki/Discrete_Fourier_transform
freq = t * sr/T

plt.subplot(122)
plt.stem(freq, np.abs(Xk.real), 'b', \
          markerfmt=" ", basefmt="-b")
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')

# Frequency domain goes all the way to 100 Hz, still, we focus on frequencies
# up to 35 Hz. 
plt.xlim(0, 35)

plt.tight_layout()
plt.savefig('FFTExample.pdf')
plt.show()