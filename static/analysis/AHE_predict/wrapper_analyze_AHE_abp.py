'''
Wrapper program to be called from the server to analyze a give 
file (such as h1-a40439-abp-mean-180min-before.csv) for AHE prediction.

Author  : Durga P
Date    : 5 June 2017
Version : 1
'''
import static.analysis.AHE_predict.svm_analyze_AHE as AH
import random
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))

def wrapper_analyze_AHE_abp(file_name):
    AHE = AH.svm_analyze_AHE(file_name)
    print('The given patient data:'),\
    file_name,', is predicted as ', AHE, '.'
    return (AHE)

    
    
