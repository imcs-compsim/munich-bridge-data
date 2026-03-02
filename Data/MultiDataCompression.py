import os
from pathlib import Path
import sys
import pyarrow.parquet as pq
import pandas as pd

in_dir = Path(
    r"P:\Projects\PhySimTwin\01 Munich bridge data\Export\Neuer Ordner")

out_dir = Path(
    r"C:\Users\bona_ja\munich-bridge-data\Data\Export\Ambient\Downsample")

# in_dir = Path(
#    r"C:\Users\bona_ja\munich-bridge-data\Data\Export\Ambient\Test")
# out_dir = os.path.join(in_dir, r"Downsample")

fns_input = sorted(in_dir.glob("*.csv"))
fn_output = os.path.join(
    out_dir, r"UniBw_2022-03-11_ref_ambient_FORCE.parquet.gzip")

cols = ['Time (-)', 'ACC01_z (g)', 'ACC02_z']
cols_strain = ['Time (-)', 'KOMP_BS (um/m)', 'KOMP_BN (um/m)', 'DMS_AS (um/m)', 'DMS_BS (um/m)',
               'DMS_CS (um/m)', 'DMS_AN (um/m)', 'DMS_BN (um/m)', 'DMS_CN (um/m)']
cols_force = ['Time (-)', 'FRC-01 (N)', 'FRC-02 (N)']

df_list = []
for i, file in enumerate(fns_input[:5]):

    print(i)

    # df_tmp = pd.read_parquet(file, columns=cols_strain)

    # df_tmp = pd.read_csv(file, usecols=cols_strain,
    #                     encoding='latin-1')

    chunk_list = []
    for chunk in pd.read_csv(
            file, usecols=cols_force, encoding='latin-1', chunksize=100_000):
        chunk_list.append(chunk)

    # Concatenate each chunk, within same file
    df_tmp = pd.concat(chunk_list)

    # Drop the first values of each sub file (huge oscillations in the sensors' readings),
    # n = 100 (0.1s) for strains
    # n = 1000 (1.0s) for forces
    n = 1000
    df_tmp = df_tmp.drop(list(range(n)))

    # Add to list, each element of the list is a file 000i:
    df_list.append(df_tmp)

df = pd.concat(df_list).reset_index(drop=True)

# Convert to datetime and calculate seconds since first instant:
df['Time (-)'] = pd.to_datetime(df['Time (-)'],
                                format='%d.%m.%Y %H:%M:%S.%f')
first_time = df['Time (-)'].iloc[0]
df['Time (s)'] = (df['Time (-)'] - first_time).dt.total_seconds()

# Set time index for resampling and resample at desired frequency:
df = df.set_index('Time (-)')

print(f"Combined DataFrame shape: {df.shape}")  # (rows, columns)

# Remove rows where ALL entries are NaN:
df = df.dropna(how='all')

# Check for additional sparse NaN values:
index = df[df.isna().any(axis=1)]
print(index)

# Export desired parquet file:
df.to_parquet(fn_output, compression='gzip')
