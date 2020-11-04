import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import copy
import time

def readcsv(data_path):
  data_ndarray = np.loadtxt(data_path + ".csv", delimiter=",")
  print("read : " + data_path + ".csv")
  return data_ndarray

readcsv()

