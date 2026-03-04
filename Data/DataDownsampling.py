import os
from pathlib import Path
import sys
import pyarrow.parquet as pq
import pandas as pd

in_dir = Path(
    r"C:\Users\bona_ja\munich-bridge-data\Data\Export\Ambient\20220404")
fn_input = os.path.join(
    in_dir, r"UniBw_2022-04-04_ref_ambient_TEMPERATURE.parquet.gzip")

df = pd.read_parquet(
    fn_input)

print(df.head)

T = 5  # (min)
df_down = df.resample("{:d}min".format(T)).mean()  # Resampling period (min)

# Remove rows where ALL entries are NaN:
df_down = df_down.dropna(how='all')

# Check for additional sparse NaN values:
index = df_down[df_down.isna().any(axis=1)]
print(index)

out_dir = os.path.join(in_dir, r"Downsample")
fn_output = os.path.join(
    # .format(int(T/1000)))
    out_dir, "UniBw_2022-04-04_ref_ambient_TEMPERATURE_5min.parquet.gzip")

# Export desired parquet file:
df_down.to_parquet(fn_output, compression='gzip')

print(df_down)
