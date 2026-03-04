import sys
from matplotlib import pyplot as plt
import pandas as pd
from scipy.signal import detrend
import numpy as np
import seaborn as sns

fn_input = r"C:\Users\bona_ja\munich-bridge-data\Data\Export\Ambient\20220404\Downsample\UniBw_2022-04-04_ref_ambient_INCLINATION_1Hz.parquet.gzip"

df = pd.read_parquet(
    fn_input)

labels = df.columns.to_list()

# Compute time differences (in seconds)
time_diffs = df.index.to_series().diff().dt.total_seconds()

# Mark points where time difference > 1 second (including the beginning)
gaps = time_diffs > 1.0
gaps[gaps.index[0]] = True
gap_indices = df.index[gaps]

# Detrend (remove effect of temperature, does it make sense?):
"""
for i in labels[2:-1]:
    x_d_linear = detrend(df[i], type='linear')
    x_line = np.array(df[i]-x_d_linear)
    df[i+' det'] = x_d_linear+x_line[0]
"""
headers = df.columns.to_list()

# Sensors' location:
x_sensor = np.array([])

colors = ['r', 'g', 'b']
fig, ax = plt.subplots(5, 2, figsize=(16, 12), dpi=300)
for i in range(5):
    for j in range(2):
        k = 2*i+j
        print(i, j, k)
        ax[i, j].plot(
            df['Time (s)'],
            df[headers[k]], '-', label=headers[k], linewidth=0.5)
        ax[i, j].legend()
        ax[i, j].set_xlabel('t (s)')
        ax[i, j].set_ylabel('inc (deg)')
        ax[i, j].grid(visible=True)
fig.tight_layout()
fig.savefig('ambient_inclination.png')
