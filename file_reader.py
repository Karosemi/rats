import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def open_file(file_path):
    try:
        data = pd.read_csv(file_path, low_memory=False)
    except UnicodeDecodeError:
        print(f'Invalid file {file_path}.')
        return None, None
    time = data.index[1:]
    try:
        if int(time[5])-int(time[4]) == 1:
            time = data['X'].values[1:]
            x = data['CH1'].values[1:]
    except ValueError:
            x = data['X'].values[1:]
    try:
        int_time = evaluate_string_data(time)
        int_x = evaluate_string_data(x)
    except UnboundLocalError:
        x = data['X'].values[1:]
    finally:
        int_x = evaluate_string_data(x)
    return int_time, int_x

def evaluate_string_data(string_data):
    int_data = []
    for str_data in string_data:
        if type(str_data) is str:
            if str_data == '-':
                pass
            else:
                try:
                    str_data = eval(str_data)
                except SyntaxError:
                    f_e = str_data.find('e')
                    s_e = str_data.find('e', f_e + 1)
                    str_data = str_data[:s_e]
                    try:
                        str_data = eval(str_data)
                    except SyntaxError:
                        str_data = str_data[:f_e]
                        str_data = eval(str_data)
                int_data.append(str_data)
        else:
            int_data.append(str_data)
    return np.array(int_data)

if __name__ == '__main__':
    time, signal = open_file('all_records/NewFile10.csv')
    plt.plot(time[100:-500], signal[100:-500])
    # indexes = np.where(time[100:-500]<-0.8)
    plt.show()
    # plt.plot(time[indexes], signal[indexes])
    # plt.show()
