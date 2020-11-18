import module
import matplotlib.pyplot as plt
import numpy as np

data_path = "/Users/touten0802/Desktop/Nakamulab/LXe/Experiment/Program_sample/001_BG_Vac_240s"
dir_path = "/Users/touten0802/Desktop/Nakamulab/LXe/Experiment/Program_sample/"
output_path = "/Users/touten0802/Desktop/Nakamulab/LXe/Experiment/Program_sample/Analysis/"

median_data_path = "/Users/touten0802/Desktop/Nakamulab/LXe/Experiment/Program_sample/Median_testdata_BG_1024x1"
medianed_data_path = "/Users/touten0802/Desktop/Nakamulab/LXe/Experiment/Program_sample/Analysis/median_test"

data = Datas()
data.read_data(dir_path, "001_BG_Vac_240s")

data = module.exp.readcsv(data_path)
filelist = module.exp.get_filename_list(dir_path)
module.exp.outcsv(data, "test", output_path)

data = module.exp.readcsv(median_data_path)
wave = [data[i][0] for i in range(len(data))]
intsy = [data[i][1] for i in range(len(data))]
intsy2 = [data[i][1] for i in range(len(data))]
medianed_data = module.exp.median(intsy)
module.exp.outcsv(medianed_data, "median_test", output_path)
data2 = module.exp.readcsv(medianed_data_path)
medianed_intsy = [data2[i] for i in range(len(data2))]

plt.plot(wave,intsy2,label="Raw_data")
plt.plot(wave,data2,label="Medianed_data")
plt.legend()
plt.show()


