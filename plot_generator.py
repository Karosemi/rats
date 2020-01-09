import os

from file_reader import open_file
from stft import get_stft, plot_stft, _get_real_time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import numpy as np

def create_plot_for_measurements(path, dir=None):
    if dir is None:
        full_path = os.path.join(path, 'plots_upper_limit')
    elif type(dir) is str:
        full_path = os.path.join(path, dir)
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    i = 0

    yell_colors = [(0.4, 0.4, 0, c) for c in np.linspace(0, 1, 1000)]
    cmapred = mcolors.LinearSegmentedColormap.from_list('mycmap', yell_colors, N=5)
    green_colors = [(173 / 255, 1, 47 / 255, c) for c in np.linspace(0, 1, 1000)]
    cmapblue = mcolors.LinearSegmentedColormap.from_list('mycmap', green_colors, N=5)
    fp = 1000
    f = np.linspace(0, 60000, fp)
    t = np.linspace(0, 2.4, int(fp * 2.4))
    Sxx = np.full((len(f), len(t)), 0)
    plt.figure(figsize=(12,6))
    plt.pcolormesh(t, f, Sxx)


    # fig = plt.figure(figsize=(8,8))
    # ax = fig.add_subplot(111)
    for file in os.listdir(path):
        # if i == 4:
        #     break
        if '.csv' in file:
            time, signal = open_file(os.path.join(path, file))
            # time = get_real_time(time)
            if time is not None:
                f, t, Sxx = get_stft(time, signal)

                png_file = os.path.join(full_path, file.replace('.csv', '.png'))
                #
                # plt.plot(Sxx)
                # ax.pcolormesh(t, f, np.abs(Sxx),  rasterized=
                plt.contourf(t, f, np.abs(Sxx), cmap=cmapred)
                plt.pcolormesh(t, f, np.abs(Sxx), cmap=cmapblue)

                # plt.hold(True)
                print(f" {png_file} plotted.")
                # i += 1
    # x0, x1 = ax.get_xlim()
    # y0, y1 = ax.get_ylim()
    # ax.imshow(img, extent=[x0, x1, y0, y1], aspect='auto')

    # fig.savefig('/tmp/test.png')
    plt.title('Spektrogram transformaty Gabora')
    plt.ylabel('Częstotliwość [Hz]')
    plt.xlabel('Czas [s]')
    upper_limit = 60000
    plt.ylim((0, upper_limit))
    plt.savefig('full_stft_all_mes3.png')
    # plt.show()
    return


def create_plots_for_measuerements(path, dir=None):
    if dir is None:
        full_path = os.path.join(path, 'plots_upper_limit')
    elif type(dir) is str:
        full_path = os.path.join(path, dir)
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    for file in os.listdir(path):
        if '.csv' in file:
            time, signal = open_file(os.path.join(path, file))
            # time = get_real_time(time)
            if time is not None:
                # f, t, Sxx = get_stft(time, signal)
                png_file = os.path.join(full_path, file.replace('.csv', '.png'))
                plot_stft(time, signal,  save=png_file, upper_limit=65000)
                print(f"File {png_file} is saved.")


if __name__ == '__main__':
    create_plot_for_measurements('./choosen')
    create_plots_for_measuerements('./choosen', 'beautiful_sounds_3')
    # fp = 43690
    # f = np.linspace(0, 60000, fp)
    # t = np.linspace(0, 2.4, int(fp * 2.4))
    # Sxx = np.full((len(f), len(t)), 0)
    # plt.pcolormesh(t, f, np.abs(Sxx))


