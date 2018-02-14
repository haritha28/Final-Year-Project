'''
Wrapper program to be called from the server to analyze a give 
file (such as h1-a40439-abp-mean-60min.csv) for AHE classification.

Author  : Durga P (rahulkrishnan@am.amrita.edu)
Date    : 5 June 2017
Version : 1
'''

import svm_analyze_AHE

def wrapper_analyze_AHE_abp(file_name):
 
# file_name = "h1-a40439-abp-mean-60min.csv"
    AHE = svm_analyze_AHE.svm_analyze_AHE(file_name)
    print 'The given patient data:',\
    file_name,', is classified as ', AHE, '.'

