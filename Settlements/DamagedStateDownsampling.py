import sys
from matplotlib import pyplot as plt
import pandas as pd

# Settlements of 1 cm, 2 cm, 3 cm.

# Load the CSV file into a DataFrame
fn_ref = [
    r"P:\Projects\PhySimTwin\01 Munich bridge data\Export\Damage scenarios\Ambient data\Settlements\UniBw_2022-04-11_support_01_ref_ambient.csv",
    r"P:\Projects\PhySimTwin\01 Munich bridge data\Export\Damage scenarios\Ambient data\Settlements\UniBw_2022-04-11_support_02_ref_ambient.csv",
]

df_tmp = pd.read_csv(
    fn_ref[0],
    encoding='latin1',
    usecols=['Time (-)', 'FRC-01 (N)', 'FRC-02 (N)'],
    # nrows=10,
    # Read 100 times per every second (Fr0 = 1000 Hz)
    skiprows=lambda i: i % 10 != 0
)

df_tmp.to_csv(
    r"C:\Users\bona_ja\munich-bridge-data\Settlements\Settlements1cmAmbientForceAt100Hz.csv",
    index=False)
