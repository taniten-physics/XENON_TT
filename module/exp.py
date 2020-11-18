import numpy as np
import matplotlib.pyplot as plt

import os


#CSVを読み込み，ndarray型で返す関数。
def readcsv(data_path):

    data_ndarray = np.loadtxt(data_path + ".csv", delimiter=",")
    print("read :" + data_path + ".csv")
    
    return data_ndarray


#指定したディレクトリのファイルネームをlistにして返す関数。拡張子は含まない。
def get_filename_list(dir_path, ext=".csv"):
    
    filename_list = []
    for f in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, f)):
            filename, fileext = os.path.splitext(f)
            if fileext == ext:
                filename_list.append(filename)
    filename_list.sort()

    return filename_list


#CSVのあるディレクトリを引数にして，data_listを返す関数。
def readcsv_datas(dir_path):
    
    filename_list = get_filename_list(dir_path)
    data_list = []
    for name in filename_list:
        data = Datas()
        data.read_data(dir_path, name)
        data_list.append(data)

    return data_list


#dataを読み込み，output_pathに出力する関数。
def outcsv(data, filename, output_path):
    
    os.makedirs(output_path, exist_ok=True)
    np.savetxt(output_path + filename + ".csv", data, delimiter=",")

    print("save :" + output_path + filename + ".csv\n")


#ルート二乗和をとる関数。
def sqrt_mean_square(a, b):
    
    val = np.sqrt(np.square(a) + np.square(b))

    return val


#Datas.data(ndarray)を受け取り，median処理を行った後のDatas.data(ndarray)を返す関数。フィルタをかけた後のデータを使って，その次の点についてフィルタをかけるようにしている。
def median(data, threshold_num=20, range_num=40):
    
    count = 0
    for i in range(len(data)):
        j = i % 1024
        if j <= range_num/2-1:
            median_val = np.median(data[:range_num])
        elif i >= 1024-range_num/2:
            median_val = np.median(data[1023-(range_num-1):])
        else:
            median_val = np.median(data[i-range_num//2:i+range_num//2])
        if data[i] > data[i-1] + threshold_num:
            data[i] = median_val
            count += 1
    print("median: {}/{} are fixed.".format(count, len(data)))

    return np.array(data)


#Datasクラスを受け取って，強度のSum（ビニング），波長の平均，誤差のRMSを計算してクラスに代入し直す関数。
def binning(datas, bin_num=128):
    
    if 1024 % bin_num != 0:
        print("ERROR : bin_num is not appropriate -> ", bin_num)
        return

    point_num = int(1024/bin_num)
    intsy_list, wave_list, error_list = [], [], []
    for i in range(point_num):
        sum_intsy = np.sum(datas.data[i*bin_num:i*bin_num+(bin_num-1)])
        mean_wave = np.mean(datas.wave[i*bin_num:i*bin_num+(bin_num-1)])
        rms_error = np.sqrt(np.sum(np.square(datas.error[i*bin_num:i*bin_num+(bin_num-1)])))
        intsy_list.append(sum_intsy)
        wave_list.append(mean_wave)
        error_list.append(rms_error)

    datas.data = np.array(intsy_list)
    datas.wave = np.array(wave_list)
    datas.error = np.array(error_list)
    datas.name += "Bin" + str(bin_num)
    datas.BINnum = bin_num

    return datas

class Datas:

    def __init__(self):

        self.name = None
        self.intsy = None
        self.wave = None
        self.error = None
        self.num = None
        self.source = None
        self.matter = None
        self.center = None
        self.intsy_type = None
        self.isError = None
        self.BINnum = None
        self.status = None

    #CSVファイルを"Datasクラス"に格納する。ファイル名からメンバ変数を決定する。実験によって適切にメンバ変数を代入する。
    def read_data(self, data_path, data_name):
        
        self.name = data_name
        attribute = data_name.split("_")
        self.num = attribute[0]
        self.source = attribute[1]
        self.matter = attribute[2]
        self.time = sttribute[3]

        if attribute.count("Nothing") == 1:
            self.source = "BG"
        elif attribute.count("BG") == 1:
            self.source = "BG"
        elif attribute.count("Sr") == 1:
            self.source = "Sr"
        elif attribute.count("Cs") == 1:
            self.source = "Cs"
        elif attribute.count("Co") == 1:
            self.source = "Co"

        if attribute.count("CsI") == 1:
            self.matter = "CsI"
        elif attribute.count("NaI") == 1:
            self.matter = "NaI"

        if attribute.count("FS") == 1:
            self.intsy_type = "FS"
        elif attribute.count("Bin") == 1:
            self.intsy_type = "Bin"

        #CSVからDatas.waveとDatas.dataを設定。FSモードに対応しており，縦に長いデータになる。
        csv = readcsv(data_path + data_name)
        if self.intsy_type == "FS":
            self.intsy = csv[:, 1:]
        else:
            self.intsy = csv[:, 1]
        wave = csv[:, 0]
        self.wave = wave[:1024]

        if attribute.count("Error") == 1 or attribute.count("Signal") == 1:
            self.error = csv[:, 2]
            self.isError = True

        #Datas.statusをファイル名から決める。
        if attribute.count("fix") == 1:
            self.status = "fix"
        if attribute.count("Median") == 1:
            self.status = "median"
        if attribute.count("Signal") == 1:
            self.status = "signal"
        if attribute.count("Cor") == 1:
            self.status = "cor"
        if attribute.count("Ref") == 1:
            self.status = "ref"
        if attribute.count("Bin") == 1:
            self.status = "bin"
            _num = attribute.index("Bin")
            self.BINnum = int(attribute[_num + 1])

    #横軸:Datas.wave，縦軸:Datas.intsyのグラフをmatplotlibを使用して作成する関数。
    def plot(self, isLabel=True, label_name=None, isZeroline=False):
        
        if isZeroline == True:
            plt.axhline(0, ls="--", color="lightslategrey", lw=3)

        if isLabel == True:
            if label_name is None:
                plt.plot(self.wave, self.intsy, label = self.name)
                plt.legned()
                return
            else:
                plt.plot(self.wave, self.intsy, label = label_name)
                plt.legend()
                return
        else:
            plt.plot(self.wave, self.data)
            return
















