import sys
from matplotlib import pyplot as plt
import pandas as pd

conditions = ['ambient', 'load', 'shaker']
fn_ref = [
    r"C:\Users\bona_ja\munich-bridge-data\ReferenceState\ReferenceStateAmbientForceAt100Hz.csv",
    r"C:\Users\bona_ja\munich-bridge-data\ReferenceState\ReferenceStateLoadForceAt100Hz.csv",
    r"C:\Users\bona_ja\munich-bridge-data\ReferenceState\ReferenceStateShakerForceAt100Hz.csv"
]

df = {}
for i, j in enumerate(conditions):
    df[j] = pd.read_csv(
        fn_ref[i],
        encoding='latin1',
        usecols=['Time (-)', 'FRC-01 (N)', 'FRC-02 (N)'])

    # Convert to datetime and calculate seconds since first instant
    df[j]['Time (-)'] = pd.to_datetime(df[j]['Time (-)'],
                                       format='%d.%m.%Y %H:%M:%S.%f')
    first_time = df[j]['Time (-)'].iloc[0]
    df[j]['Time (s)'] = (df[j]['Time (-)'] -
                         first_time).dt.total_seconds()

labels = ['south', 'north']
colors = ['r', 'g', 'b']
fig, ax = plt.subplots(1, 1, figsize=(12, 6), dpi=300)
ax.plot(
    df['shaker']['Time (s)'],
    df['shaker']['FRC-01 (N)']/1.0E+03, '-', label=labels[0], color=colors[0])
ax.plot(
    df['shaker']['Time (s)'],
    df['shaker']['FRC-02 (N)']/1.0E+03, '-', label=labels[1], color=colors[1])
ax.legend()
ax.set_xlabel('t (s)')
ax.set_ylabel('F (kN)')
ax.grid(visible=True)
fig.tight_layout()
fig.savefig('reaction_forces_.png')

sys.exit()


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
