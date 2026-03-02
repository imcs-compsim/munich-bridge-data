import sys
from matplotlib import pyplot as plt
import pandas as pd
from scipy.signal import detrend
import numpy as np
import seaborn as sns

fn_input = r"C:\Users\bona_ja\munich-bridge-data\Data\Export\Ambient\Downsample\UniBw_2022-03-11_ref_ambient_STRAIN_1Hz.parquet.gzip"

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
for i in labels[2:-1]:
    x_d_linear = detrend(df[i], type='linear')
    x_line = np.array(df[i]-x_d_linear)
    df[i+' det'] = x_d_linear+x_line[0]
labels = df.columns.to_list()

# Sensors' location:
x_sensor = np.array([5.97, 14.95, 24.30])

colors = ['r', 'g', 'b']
fig, ax = plt.subplots(1, 1, figsize=(12, 6), dpi=300)
for i, j in enumerate([labels[2:8]]):
    ax.plot(
        df['Time (s)'],
        df[j], '-', label=j, linewidth=1.0)
    # Add markers for each recording session:
    ax.plot(
        df.loc[gaps, 'Time (s)'],
        df.loc[gaps, j], 'o')
ax.legend()
ax.set_xlabel('t (s)')
ax.set_ylabel('epel (um/m)')
ax.grid(visible=True)
fig.tight_layout()
plt.show()
# fig.savefig('ambient_strains.png')

"""counts, bins = np.histogram(df[labels[2]+'_detrend'], bins=250)
fig, ax = plt.subplots(1, 1, figsize=(12, 6), dpi=300)
sns.histplot(data=df[labels[2]+'_detrend'], ax=ax)
# ax.hist(bins[:-1], bins, weights=counts)
ax.legend()
ax.grid(visible=True)
fig.tight_layout()
fig.savefig('ambient_strains_hist.png')"""
