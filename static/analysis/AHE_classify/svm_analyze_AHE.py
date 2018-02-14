'''
Author	: Durga P
Program : To classify patient abp data as AHE or not
Date 	: 5 June 2017
Version	: 1
'''
#import packages
import numpy as np
import pandas as pd
from sklearn.externals import joblib

def svm_analyze_AHE(file_name):

    # obtain abp file
    testdata = pd.read_csv(file_name, header=None)
    print "TESTDATA"
    print testdata
    testdata_to_transpose = testdata.iloc[1 :,1]
    print "TESTTORESPONSE"
    print testdata_to_transpose
    testdata = np.transpose(testdata_to_transpose)
    testdata = testdata.reshape(1, -1)
    print "RESHAPE"
    print testdata

    # extract abp values
    print testdata.shape
    leng = testdata.shape[1]
    #print leng
    testdata =  np.array(testdata[:,0:(leng-1)])
    

    # once model is stored, then retrieve it
    model = joblib.load('svm-model-0.pkl') 

    # make predictions
    predicted = model.predict(testdata)

    return predicted


