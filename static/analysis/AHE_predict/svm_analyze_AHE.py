'''
Author	: Durga P
Program : To predict patient abp data as AHE or not
Date 	: 5 June 2017
Version	: 1
'''
#import packages
import numpy as np
import pandas as pd
from sklearn.externals import joblib
import numpy
def svm_analyze_AHE(file_name):

    # obtain abp file
    testdata = pd.read_csv(file_name, header=None)
    #print testdata
    testdata_to_transpose = testdata.iloc[:,1]
    #print testdata_to_transpose
    testdata = np.transpose(testdata_to_transpose)
    testdata = testdata.reshape(1, -1)
    #print testdata

    # extract abp values
    #print testdata.shape
    leng = testdata.shape[1]-1
    #print leng
    #T = testdata.iloc[:,leng]
    T =  np.array(testdata[:,0:leng])
    #print T
    testdata = np.array(T)

    # once model is stored, then retrieve it
    model = joblib.load('svm-model-0.pkl') 

    # make predictions
    predicted = model.predict(testdata)
    isinstance(predicted, (numpy.ndarray,))  #### This is the fix
    return predicted.tolist()

    #return predicted

