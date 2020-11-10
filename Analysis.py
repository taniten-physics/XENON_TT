import module

data_path = "/Users/touten0802/Desktop/Nakamulab/LXe/Experiment/Program_sample/001_BG_GXe_240s"
dir_path = "/Users/touten0802/Desktop/Nakamulab/LXe/Experiment/Program_sample/"
output_path = "/Users/touten0802/Desktop/Nakamulab/LXe/Experiment/Program_sample/Analysis/"

data = module.exp.readcsv(data_path)
filelist = module.exp.get_filename_list(dir_path)
module.exp.outcsv(data, "test", output_path)

