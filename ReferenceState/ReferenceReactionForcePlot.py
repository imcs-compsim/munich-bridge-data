import sys
from matplotlib import pyplot as plt
import pandas as pd
from scipy.signal import detrend
import numpy as np
import seaborn as sns


def fun(x, t):
    coef = np.array([7.14360177,  0.08154961, -2.14779907, -0.32518481])
    return x*(coef@np.array([t**0, t**1, t**2, t**3]))


y = fun(1, 5000)

print(y)
sys.exit()

fn_input = r"C:\Users\bona_ja\munich-bridge-data\Data\Export\Ambient\20220404\Downsample\UniBw_2022-04-04_ref_ambient_FORCE_1Hz.parquet.gzip"

df = pd.read_parquet(
    fn_input)

labels = df.columns.to_list()

coef = np.array([7.14360177,  0.08154961, -2.14779907, -0.32518481])

# Detrend (remove effect of temperature, does it make sense?):
"""
for i in labels[:1]:
    x_d_linear = detrend(df[i], type='linear')
    x_line = np.array(df[i]-x_d_linear)
    df[i+' det'] = x_d_linear+x_line[0]
"""

sys.exit()

headers = df.columns.to_list()

# Compute time differences (in seconds)
time_diffs = df.index.to_series().diff().dt.total_seconds()

# Mark points where time difference > 1 second (including the beginning)
gaps = time_diffs > 1.0
gaps[gaps.index[0]] = True
gap_indices = df.index[gaps]

colors = ['r', 'g', 'b']
labels = ['south', 'north']
fig, ax = plt.subplots(1, 1, figsize=(12, 6), dpi=300)
for i, j in enumerate(headers[:2]):
    ax.plot(
        df.index,
        df[j]/1.0E+03, '-', label=labels[i], linewidth=1.0)
    # Add markers for each recording session:
#    ax.plot(
#        df.index[gaps],
#        df.loc[gaps, j]/1.0E+03, 'o')
#    ax.plot(
#        df.index,  # ['Time (s)'],
#        x_line/1.0E+03)
ax.legend()
ax.set_xlabel('t (s)')
ax.set_ylabel('F (kN)')
ax.grid(visible=True)
fig.tight_layout()
# plt.show()
fig.savefig('ambient_forces.png')

"""counts, bins = np.histogram(df[labels[2]+'_detrend'], bins=250)
fig, ax = plt.subplots(1, 1, figsize=(12, 6), dpi=300)
sns.histplot(data=df[labels[2]+'_detrend'], ax=ax)
# ax.hist(bins[:-1], bins, weights=counts)
ax.legend()
ax.grid(visible=True)
fig.tight_layout()
fig.savefig('ambient_strains_hist.png')"""
