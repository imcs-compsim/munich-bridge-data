"""
The considered files (DMS..., see below) contain the strain measurements of 
multiple crossings of our test car across the bridge. Always two crossings are
recorded for the same state of the bridge (undamaged, 1cm, 2cm, and 3cm support
settlement).

The goal is to identify the pairs based on the relative strain data.
"""

import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

import skfda.preprocessing.smoothing.kernel_smoothers as ks
from skfda.preprocessing.smoothing.kernel_smoothers import (
    NadarayaWatsonSmoother,
)
import skfda
from skfda.preprocessing.registration import (
    FisherRaoElasticRegistration,
    invert_warping,
)
from skfda.misc.metrics._fisher_rao import fisher_rao_distance

date = "2022-04-11"

formatter = mdates.DateFormatter("%H:%M")

suffix = "DMS_CNAt" + "100" + "Hz"

file_names = [
    "../Settlements/UniBw_" + date + "_ref_support_load_01",
    "../Settlements/UniBw_" + date + "_support_load_01",
    "../Settlements/UniBw_" + date + "_support_load_02",
    "../Settlements/UniBw_" + date + "_support_load_03",
]

data = {}

# read data
for file in file_names:
    data[file] = pd.read_csv(file + suffix + ".csv.zip")
    data[file]["Time (-)"] = pd.to_datetime(data[file]["Time (-)"])


# x_col_name = 'Time (-)'
# y_col_name = 'DMS_CN (um/m)'
####################----------------------------------------------------
# Here we define slicing locations
incr = 4500
start_1 = [4500, 3850, 4150, 4850]
start_2 = [51800, 50850, 50750, 51700]

start1_dict = {list(data.keys())[i]: start_1[i] for i in range(len(start_1))}
start2_dict = {list(data.keys())[i]: start_2[i] for i in range(len(start_2))}

# define empty dictionaries for each crossings (total 2: going forward and coming back)
df_sliced_cross_1 = {}
df_sliced_cross_2 = {}

# do slicing
for i, df_name in enumerate(data.keys()):
    df = data[df_name]
    df_sliced_name = df_name + "_sliced"
    df_sliced_cross_1[df_sliced_name] = df[
        start1_dict[df_name] : start1_dict[df_name] + incr
    ].copy()
    df_sliced_cross_2[df_sliced_name] = df[
        start2_dict[df_name] : start2_dict[df_name] + incr
    ].copy()

# flag for showing slicing locations, if we set it True, we can visualize so that if they were set approximately correct.
plot_red_lines = False
if plot_red_lines:
    fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(20, 10))

    for i, df_name in enumerate(data.keys()):

        df = data[df_name]
        curAx = ax.flat[i]
        df.plot(ax=curAx, x="Time (-)", y="DMS_CN (um/m)", x_compat=True)

        ax[i].axvline(
            df.iloc[start1_dict[df_name], 0], color="r", linestyle="--", lw=2
        )
        ax[i].axvline(
            df.iloc[start1_dict[df_name] + incr, 0],
            color="r",
            linestyle="--",
            lw=2,
        )
        ax[i].axvline(
            df.iloc[start2_dict[df_name], 0], color="r", linestyle="--", lw=2
        )
        ax[i].axvline(
            df.iloc[start2_dict[df_name] + incr, 0],
            color="r",
            linestyle="--",
            lw=2,
        )

        curAx.get_legend().remove()

        curAx.set_xlabel(" ")
        # curAx.xaxis.set_label_coords(-0.1, -0.17)
        curAx.xaxis.set_major_formatter(formatter)
        curAx.xaxis.set_major_locator(MaxNLocator(75))
    plt.subplots_adjust(
        left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4
    )
    # plt.setp( curAx.xaxis.get_ticklabels(), rotation=35, ha="right", rotation_mode="anchor")
    plt.show()

# FischerRao distance need FDataGrid to be defined.
def generate_datagrid(grid_points, data_matrix, scaled=False):
    if scaled:
        # grid_points = grid_points/grid_points.max()
        grid_points_std = (grid_points - grid_points.min()) / (
            grid_points.max() - grid_points.min()
        )
        data_matrix_std = (data_matrix - data_matrix.min()) / (
            data_matrix.max() - data_matrix.min()
        )
        data_matrix = data_matrix_std
        grid_points = grid_points_std
    else:
        grid_points = grid_points - grid_points.min()
    data_grid = skfda.FDataGrid(
        data_matrix=data_matrix, grid_points=grid_points
    )
    return data_grid


# Here we plot sliced data and calculate Fisher-Rao distances without smoothing
plot_sliced_data = True
calculate_fisher_rao_distance = True

if plot_sliced_data:
    fig, axs = plt.subplots(2, 4, figsize=(12, 6))
    # df_name_0 = list(df_sliced_cross_1.keys())[0]
    fd_global = {}
    for i, df in enumerate(df_sliced_cross_1):
        axs[0, i].plot(
            df_sliced_cross_1[df].iloc[:, 0], df_sliced_cross_1[df].iloc[:, 1]
        )
        axs[0, i].xaxis.set_major_formatter(formatter)
        axs[0, i].xaxis.set_major_locator(MaxNLocator(5))
        plt.setp(
            axs[0, i].xaxis.get_ticklabels(),
            rotation=25,
            ha="right",
            rotation_mode="anchor",
        )
        if calculate_fisher_rao_distance:
            data_matrix = df_sliced_cross_1[df].iloc[:, 1].to_numpy()
            grid_points = df_sliced_cross_1[df].index.to_numpy()
            fd = generate_datagrid(grid_points, data_matrix, scaled=False)
            df = df + "_1"
            fd_global[df] = fd

    for i, df in enumerate(df_sliced_cross_2):
        axs[1, i].plot(
            df_sliced_cross_2[df].iloc[:, 0], df_sliced_cross_2[df].iloc[:, 1]
        )
        axs[1, i].xaxis.set_major_formatter(formatter)
        axs[1, i].xaxis.set_major_locator(MaxNLocator(5))
        plt.setp(
            axs[1, i].xaxis.get_ticklabels(),
            rotation=25,
            ha="right",
            rotation_mode="anchor",
        )
        if calculate_fisher_rao_distance:
            data_matrix = df_sliced_cross_2[df].iloc[:, 1].to_numpy()
            grid_points = df_sliced_cross_2[df].index.to_numpy()
            fd = generate_datagrid(grid_points, data_matrix, scaled=False)
            df = df + "_2"
            fd_global[df] = fd

    rows = ["East-To-West-Crossing 1", "East-To-West-Crossing 2"]
    cols = ["Reference", "Settl. (1 cm)", "Settl. (2 cm)", "Settl. (3 cm)"]

    fisher_global = np.zeros((8, 8))
    for i, fd_1_name in enumerate(fd_global.keys()):
        for j, fd_2_name in enumerate(fd_global.keys()):
            fd_1 = fd_global[fd_1_name]
            fd_2 = fd_global[fd_2_name]
            fisher_global[i, j] = float(fisher_rao_distance(fd_1, fd_2))

    for ax, col in zip(axs[0], cols):
        ax.set_title(col)

    for ax, row in zip(axs[:, 0], rows):
        ax.set_ylabel(row, rotation=90, size="large")

    plt.savefig("strain_original.png", dpi=300)

    fig = plt.figure(figsize=(12, 12))
    ax = plt.gca()
    im = ax.matshow(fisher_global, interpolation="none")
    cbar = fig.colorbar(im, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=15)
    for (i, j), z in np.ndenumerate(fisher_global):
        ax.text(
            j, i, "{:0.2f}".format(z), ha="center", va="center", fontsize=17
        )
    tickets = [
        "Ref_1",
        "Settl_1\n (1 cm)",
        "Settl_1\n (2 cm)",
        "Settl_1\n (3 cm)",
        "Ref_2",
        "Settl_2\n (1 cm)",
        "Settl_2\n (2 cm)",
        "Settl_2\n (3 cm)",
    ]
    ax.set_xticks(np.arange(len(tickets)), labels=tickets)
    ax.set_yticks(np.arange(len(tickets)), labels=tickets)

    # Rotate the tick labels and set their alignment.
    plt.setp(
        ax.get_xticklabels(),
        rotation=-20,
        ha="right",
        rotation_mode="anchor",
        fontsize=18,
    )
    plt.setp(ax.get_yticklabels(), fontsize=18)
    plt.tight_layout()
    plt.savefig("compare_original.png", dpi=300)

# Here we plot sliced data and calculate Fisher-Rao distances with smoothing
plot_sliced_smooth_data = True
calculate_fisher_rao_distance = True
smoother = ks.LocalLinearRegressionSmoother(
    smoothing_parameter=0.05
)  # 0.05 -->scaling 4 -->

if plot_sliced_smooth_data:
    fig, axs = plt.subplots(2, 4, figsize=(12, 6))
    # df_name_0 = list(df_sliced_cross_1.keys())[0]
    fd_global = {}
    for i, df in enumerate(df_sliced_cross_1):
        data_matrix = df_sliced_cross_1[df].iloc[:, 1].to_numpy()
        grid_points = df_sliced_cross_1[df].index.to_numpy()
        fd = generate_datagrid(grid_points, data_matrix, scaled=True)
        fd = smoother.fit_transform(fd)
        df_temp = df + "_1"
        fd_global[df_temp] = fd

        axs[0, i].plot(
            df_sliced_cross_1[df].iloc[:, 0], fd.data_matrix[0].flatten()
        )
        axs[0, i].xaxis.set_major_formatter(formatter)
        axs[0, i].xaxis.set_major_locator(MaxNLocator(5))
        plt.setp(
            axs[0, i].xaxis.get_ticklabels(),
            rotation=25,
            ha="right",
            rotation_mode="anchor",
        )

    for i, df in enumerate(df_sliced_cross_2):
        data_matrix = df_sliced_cross_2[df].iloc[:, 1].to_numpy()
        grid_points = df_sliced_cross_2[df].index.to_numpy()
        fd = generate_datagrid(grid_points, data_matrix, scaled=True)
        fd = smoother.fit_transform(fd)
        df_temp = df + "_2"
        fd_global[df_temp] = fd

        axs[1, i].plot(
            df_sliced_cross_1[df].iloc[:, 0], fd.data_matrix[0].flatten()
        )
        axs[1, i].xaxis.set_major_formatter(formatter)
        axs[1, i].xaxis.set_major_locator(MaxNLocator(5))
        plt.setp(
            axs[1, i].xaxis.get_ticklabels(),
            rotation=25,
            ha="right",
            rotation_mode="anchor",
        )

    rows = ["East-To-West-Crossing 1", "East-To-West-Crossing 2"]
    cols = ["Reference", "Settl. (1 cm)", "Settl. (2 cm)", "Settl. (3 cm)"]

    fisher_global = np.zeros((8, 8))
    for i, fd_1_name in enumerate(fd_global.keys()):
        for j, fd_2_name in enumerate(fd_global.keys()):
            if i == j:
                fisher_global[i, j] = 0.0
                fisher_global[j, i] = fisher_global[i, j]
                continue
            if j <= i:
                continue
            fd_1 = fd_global[fd_1_name]
            fd_2 = fd_global[fd_2_name]
            fisher_global[i, j] = float(fisher_rao_distance(fd_1, fd_2))
            fisher_global[j, i] = fisher_global[i, j]

    for ax, col in zip(axs[0], cols):
        ax.set_title(col)

    for ax, row in zip(axs[:, 0], rows):
        ax.set_ylabel(row, rotation=90, size="large")

    plt.savefig("strain_smooth.png", dpi=300)

    fig = plt.figure(figsize=(12, 12))
    ax = plt.gca()
    im = ax.matshow(fisher_global, interpolation="none")
    cbar = fig.colorbar(im, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=15)
    for (i, j), z in np.ndenumerate(fisher_global):
        ax.text(
            j, i, "{:0.2f}".format(z), ha="center", va="center", fontsize=17
        )
    tickets = [
        "Ref_1",
        "Settl_1\n (1 cm)",
        "Settl_1\n (2 cm)",
        "Settl_1\n (3 cm)",
        "Ref_2",
        "Settl_2\n (1 cm)",
        "Settl_2\n (2 cm)",
        "Settl_2\n (3 cm)",
    ]
    ax.set_xticks(np.arange(len(tickets)), labels=tickets)
    ax.set_yticks(np.arange(len(tickets)), labels=tickets)

    # Rotate the tick labels and set their alignment.
    plt.setp(
        ax.get_xticklabels(),
        rotation=-20,
        ha="right",
        rotation_mode="anchor",
        fontsize=18,
    )
    plt.setp(ax.get_yticklabels(), fontsize=18)
    plt.tight_layout()
    plt.savefig("compare_smooth.png", dpi=300)
