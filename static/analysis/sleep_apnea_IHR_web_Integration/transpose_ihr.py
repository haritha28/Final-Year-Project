'''Aum
Program  to transpose row-wise arranged IHR values
Author : Dhara Prathap
Date   : 30-May-2017
Version: v1
'''
import math
from scipy import stats
import numpy as np
import pandas as pd
import sys, getopt
import csv

def transpose_ihr(file_name):
    output_filename = "trans.csv"
    i = 0;
    my_data = pd.read_csv(file_name, header=None)
    ihr = np.array(my_data[:])

    ihr = ihr.reshape(-1, 1)
    x = my_data.iloc[:, 2]
    y = my_data.iloc[:, 1]
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    start_index = 0
    t = 60
    f = open(output_filename, "a+")

    for i in range (0, len(x)):
        if x[i] > t:
                a = np.array(y[start_index : i])    
                trans = np.transpose(a)
                trans = trans.ravel()
                trans = trans.tolist()
                b = len(trans)
                if b < 30:
                    for idx, item in enumerate(trans):
                        if idx == len(trans)-1:
                           a = item
                    for i in range(b-1, 31):
                        trans.insert(i, a)
                trans = np.array(trans)
                trans1 = np.array([trans[:30]])
                start_index = i                             # store start index for next 60s data series
                t = t + 60
                np.savetxt(f, trans1, fmt="%3.2f", delimiter=',', newline='\n')
    f.close()
    return output_filename
