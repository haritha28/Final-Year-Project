'''
Author	: Durga P
Program : To predict AHE
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
    #print testdata
    testdata_to_transpose = testdata.iloc[:,1]
    #print testdata_to_transpose
    testdata = np.transpose(testdata_to_transpose)
    testdata = testdata.reshape(1, -1)
    #print testdata

    # extract abp values
    #print testdata.shape
    leng = testdata.shape[1]
    #print leng
    testdata =  np.array(testdata[:,0:(leng-1)])
    

    # once model is stored, then retrieve it
    model = joblib.load('svm-model-0.pkl') 

    # make predictions
    predicted = model.predict(testdata)
    predicted1 = model.predict_proba(testdata)

    # summarize the fit of the model
    np.savetxt('RFpredicted.txt', predicted1)

    #save predicted labels to a csv file
    y_pred = predicted
    predicted = model.predict_proba(testdata)
    #np.savetxt("svmrbfpred.csv", clas)

    return y_pred



'''
----------------------------------------------------------
def svm_analyze_AHE(file_name):

    #take test data file
    testdata = pd.read_csv(file_name, header=None)
    print testdata
    testdata_to_transpose = testdata.iloc[25,:]
    #print testdata_to_transpose
    testdata = np.transpose(testdata_to_transpose)
    testdata = testdata.reshape(1, -1)
    print testdata

    #take ihr values
    print testdata.shape
    leng = testdata.shape[1]-1
    print leng
    #T = testdata.iloc[:,leng]
    testdata =  np.array(testdata[:, 0:leng])
    #print T
    #testdata = np.array(T)

    # once model is stored, then retrieve it
    model = joblib.load('svm-model-0.pkl') 
    #model.setThreshold(0.5)
    # make predictions
    predicted = model.predict(testdata)
    print predicted
    predicted1 = model.predict_proba(testdata)
    print predicted1 
    # summarize the fit of the model
    np.savetxt('RFpredicted.txt', predicted1)

    #save preedicted labels to a csv file
    y_pred = predicted
    predicted = model.predict_proba(testdata)
    #np.savetxt("svmrbfpred.csv", clas)

    return y_pred
'''
