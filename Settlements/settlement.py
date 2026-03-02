import sys
from matplotlib import pyplot as plt
import pandas as pd

# Load the CSV file into a DataFrame
fn_amb = [
    r"P:\Projects\PhySimTwin\01 Munich bridge data\Export\Damage scenarios\Ambient data\Settlements\UniBw_2022-04-11_support_01_ref_ambient.csv",
    r"P:\Projects\PhySimTwin\01 Munich bridge data\Export\Damage scenarios\Ambient data\Settlements\UniBw_2022-04-11_support_02_ref_ambient.csv",
    r"P:\Projects\PhySimTwin\01 Munich bridge data\Export\Damage scenarios\Ambient data\Settlements\UniBw_2022-04-11_support_03_ref_ambient_0001.csv"]

fn_load_tests = [
    r"P:\Projects\PhySimTwin\01 Munich bridge data\Export\Damage scenarios\Load tests\Settlements\UniBw_2022-04-11_support_load_01.csv",
    r"P:\Projects\PhySimTwin\01 Munich bridge data\Export\Damage scenarios\Load tests\Settlements\UniBw_2022-04-11_support_load_02.csv",
    r"P:\Projects\PhySimTwin\01 Munich bridge data\Export\Damage scenarios\Load tests\Settlements\UniBw_2022-04-11_support_load_03.csv"]

df = {'ambient': {}, 'load': {}}
n_samples = 2000

for i, j in enumerate(fn_amb):
    df['ambient'][i] = pd.read_csv(
        j,
        encoding='latin1',
        nrows=n_samples,
        usecols=['Time (-)', 'FRC-01 (N)', 'FRC-02 (N)'])

    # Convert to datetime and calculate seconds since first instant
    df['ambient'][i]['Time (-)'] = pd.to_datetime(df['ambient'][i]['Time (-)'],
                                                  format='%d.%m.%Y %H:%M:%S.%f')
    first_time = df['ambient'][i]['Time (-)'].iloc[0]
    df['ambient'][i]['Time (s)'] = (df['ambient'][i]['Time (-)'] -
                                    first_time).dt.total_seconds()

for i, j in enumerate(fn_load_tests):
    df['load'][i] = pd.read_csv(
        j,
        encoding='latin1',
        nrows=n_samples,
        usecols=['Time (-)', 'FRC-01 (N)', 'FRC-02 (N)'])

    # Convert to datetime and calculate seconds since first instant
    df['load'][i]['Time (-)'] = pd.to_datetime(df['load'][i]['Time (-)'],
                                               format='%d.%m.%Y %H:%M:%S.%f')
    first_time = df['load'][i]['Time (-)'].iloc[0]
    df['load'][i]['Time (s)'] = (df['load'][i]['Time (-)'] -
                                 first_time).dt.total_seconds()

# Print the first 20 rows
# print(df['ambient'][0].head(20))

labels = ['1 cm', '2 cm', '3 cm']
colors = ['r', 'g', 'b']

fig, ax = plt.subplots(2, 1, figsize=(12, 6), dpi=300)
for i in range(3):
    ax[0].plot(
        df['ambient'][i]['Time (s)'],
        df['ambient'][i]['FRC-01 (N)']/1.0E+03, '-', label=labels[i], color=colors[i], marker='o', markevery=100)
    ax[0].plot(
        df['load'][i]['Time (s)'],
        df['load'][i]['FRC-01 (N)']/1.0E+03, '-', label=labels[i], color=colors[i], marker='x', markevery=100)
    ax[1].plot(
        df['ambient'][i]['Time (s)'],
        df['ambient'][i]['FRC-02 (N)']/1.0E+03, '-', label=labels[i], color=colors[i], marker='o', markevery=100)
    ax[1].plot(
        df['load'][i]['Time (s)'],
        df['load'][i]['FRC-02 (N)']/1.0E+03, '-', label=labels[i], color=colors[i], marker='x', markevery=100)
ax[0].set_title('Support South')
ax[1].set_title('Support North')

for i in range(2):
    ax[i].legend()
    ax[i].set_xlabel('t (s)')
    ax[i].set_ylabel('F (kN)')

fig.tight_layout()
fig.savefig('reaction_forces.png')
