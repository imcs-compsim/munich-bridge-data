import sys
from matplotlib import pyplot as plt
import pandas as pd
from scipy.signal import detrend
import numpy as np
import seaborn as sns

fn_input = r"C:\Users\bona_ja\munich-bridge-data\Data\Export\Ambient\20220404\Downsample\UniBw_2022-04-04_ref_ambient_TEMPERATURE_5min.parquet.gzip"

df = pd.read_parquet(
    fn_input)

labels = df.columns.to_list()

# Temperature fit:
deg = 3
poly_temp_fit = np.polynomial.Polynomial.fit(
    df['Time (s)'], df['Air Temperature -  (°C)'], deg)
df['Air Temperature Poly -  (°C)'] = poly_temp_fit(df['Time (s)'])

fig, ax = plt.subplots(1, 1, figsize=(12, 6), dpi=300)
ax.plot(
    df['Time (s)'],
    df['Air Temperature -  (°C)'], '-o', label=labels[0], linewidth=1.0)
ax.plot(
    df['Time (s)'],
    df['Air Temperature Poly -  (°C)'], '-', label='Poly fit', linewidth=1.0)

ax.set_xlabel('t (s)')
ax.set_ylabel('T (°C)')
ax.legend()
ax.grid(visible=True)
fig.tight_layout()
# plt.show()
fig.savefig('ambient_temperature.png')
