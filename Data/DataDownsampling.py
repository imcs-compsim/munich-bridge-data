import os
from pathlib import Path
import sys
import pyarrow.parquet as pq
import pandas as pd

in_dir = Path(r"C:\Users\bona_ja\munich-bridge-data\Data\Export\Ambient")
fn_input = os.path.join(
    in_dir, r"UniBw_2022-03-11_ref_ambient_FORCE.parquet.gzip")

df = pd.read_parquet(
    fn_input)

print(df.head)

T = 1000  # (ms)
df_down = df.resample("{:d}ms".format(T)).mean()  # Resampling period (ms)

# Remove rows where ALL entries are NaN:
df_down = df_down.dropna(how='all')

# Check for additional sparse NaN values:
index = df_down[df_down.isna().any(axis=1)]
print(index)

out_dir = os.path.join(in_dir, r"Downsample")
fn_output = os.path.join(
    out_dir, "UniBw_2022-03-11_ref_ambient_FORCE_{:d}Hz.parquet.gzip".format(int(T/1000)))

# Export desired parquet file:
df_down.to_parquet(fn_output, compression='gzip')
