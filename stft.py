import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import pandas as pd
from file_reader import open_file, open_csv_file

def plot_fft(time, signal, fp=None, freq_limit=60000,save=None):
    freqs, fft = get_fft(time, signal, fp)
    half_freqs, half_fft = freqs[:freqs.size//2], fft[:fft.size//2]
    m_fft = np.abs(half_fft)
    quant = np.quantile(m_fft, 0.90)
    half_fft = np.where(m_fft<quant, 0, half_fft)
    freqs_limit_index = np.argmin(np.abs(half_freqs - freq_limit))
    plt.style.use('ggplot')
    plt.figure(figsize=(12,6))
    plt.plot(half_freqs[100:], np.abs(half_fft)[100:])
    plt.title('Moduł Transformaty Fouriera')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Amplituda [V')
    # plt.ylim((0, np.max(np.abs(half_fft[100:])))
    if np.max(freqs) >= freq_limit:
        plt.xlim((0,half_freqs[freqs_limit_index]))
    if save is not None:
        plt.savefig(save)

    else:
        plt.show()
    plt.close()


def plot_stft(time, signal, fp=None, save=None, upper_limit=65000, time_signal=False):
    """

    :param f: frequency range
    :param t: time
    :param Sxx: Short Time Fourier Transform
    :param save: save file name, if None then plot printed, but is not saved
    :param upper_limit: upper frequency limit of plot
    """
    f, t, Sxx = get_stft(time, signal, fp)
    if f is None:
        return None
    plt.figure(figsize=(12, 12))
    if time_signal:
        plt.subplot(211)
        plt.plot(time, signal)
        plt.title('Time signal')
        plt.xlabel('Time [sec]')
        plt.ylabel('Amplitude')
        plt.subplot(212)
    plt.pcolormesh(t+np.min(time), f, np.abs(Sxx), vmax=0.5)
    plt.title('Spektrogram transformaty Gabora')
    plt.ylabel('Częstotliwość [Hz]')
    plt.xlabel('Czas [s]')
    if np.max(f) >= upper_limit:
        plt.ylim((0, upper_limit))
    if save is not None:
        plt.savefig(save)
    else:
        plt.show()
    plt.close()


def get_fft(time, signal, fp):
    if fp is None:
        fp = find_fp(time)
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(signal.size, 1 / fp)
    return freqs, fft


def get_stft(time, signal, fp = None, nperseg=4096//2, std = 100):
    """
    :param time: time array
    :param signal: measuerement array
    :param nperseg: window weight
    :return:
    """
    if fp is None:
        fp = find_fp(time)
    wind = sig.get_window(('gaussian', std), nperseg)
    try:
        f, t, Sxx = sig.stft(signal, fs=fp, window=wind, nperseg=nperseg, return_onesided=True, noverlap=int(0.9*nperseg))
    except ValueError:
        return None, None, None
    return f, t, Sxx

def _get_real_time(time):
    min_t = abs(np.min(time))
    for i in range(len(time)):
        time[i] = time[i] + min_t
    return time

def find_fp(time):
    beg = time.size // 8
    end = time.size // 8 + time.size // 8
    cut_beg_time = time[beg:]
    beg_time = time[beg]
    end_time = time[end]
    beg_oth_time = time[beg]
    i = 1
    while beg_oth_time == beg_time:
        beg_oth_time = cut_beg_time[i]
        i += 1
    j = 1
    end_oth_time = time[end]
    cut_end_time = time[end:]
    while end_oth_time == end_time:
        end_oth_time = cut_end_time[j]
        j += 1

    duration = end_oth_time - beg_oth_time
    cut_time = time[beg + i:end + j]
    fp = get_sampling_rate(cut_time.size, duration)
    return fp

def get_sampling_rate(N, duration):
    """
    :param N: number of samples
    :param duration: measuerement duration time
    :return: sampling rate
    """
    return N/duration

# if __name__ == '__main__':
#     file = 'all_records/NewFile10.csv'
#     time, signal = open_file(file)
    # fft = np.fft.fft(signal)
    # quant = np.quantile(np.abs((fft)), 0.9)
    # fft = np.where(np.abs(fft)<quant, 0, fft)
    # new_signal = np.real(np.fft.ifft(fft))
    # time = _get_real_time(time)
    # plt.hist(signal, bins = 100)
    # plt.show()
    # plt.style.use('ggplot')
    # plt.plot(time, new_signal)
    # plt.show()
    # plt.title('Sygnał czasowy')
    # plt.xlabel('Czas [s]')
    # plt.ylabel('Amplituda [V]')
    # plt.savefig('sygnal_czasowy.png')
    # plot_stft(time, signal, upper_limit=50000, save='stft_1.png')
    # df = pd.read_csv(file)
    # time = df['time'].values
    # signal = df['signal'].values
    # plot_fft(time[:100000], signal[:10000], save='uciety_fourier.png')