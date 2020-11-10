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


class Datas:

    def __init__(self):

        self.name = None
        self.data = None
        self.wave = None
        self.error = None
        self.num = None
        self.source = None
        self.matter = None
        self.center = None
        self.data_type = None
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
            self.data_type = "FS"
        elif attribute.count("Bin") == 1:
            self.data_type = "Bin"

        #CSVからDatas.waveとDatas.dataを設定。FSモードに対応しており，縦に長いデータになる。
        csv = readcsv(data_path + data_name)
        if self.data_type == "FS":
            self.data = csv[:, 1:]
        else:
            self.data = csv[:, 1]
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

