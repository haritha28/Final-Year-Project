'''
Author	: Dhara Prathap J
Program : to analyse/predict sleep apnea with AHI
Date 	: 2 June 2017
Version	: 3
'''
#import packages
import numpy as np
import pandas as pd
from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDClassifier
from sklearn.cross_validation import train_test_split
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Normalizer
import numpy as np
import pandas as pd
from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDClassifier
from sklearn.cross_validation import train_test_split
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Normalizer
import numpy as np
import pandas as pd
from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDClassifier
from sklearn.cross_validation import train_test_split
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Normalizer
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error, roc_curve, classification_report,auc)
from sklearn.externals import joblib

def svm_analyze_ihr(file_name):

    #take test data file
    testdata = pd.read_csv(file_name, header=None, delim_whitespace=True)

    #take ihr values
    T = testdata.iloc[:,1:31]
    scaler = Normalizer().fit(T)
    testT = scaler.transform(T)
    testdata = np.array(testT)

    # once model is stored, then retrieve it
    model = joblib.load('svm-model-1.pkl') 

    # make predictions
    predicted = model.predict(testdata)
    predicted1 = model.predict_proba(testdata)

    # summarize the fit of the model
    np.savetxt('RFpredicted.txt', predicted1)

    #save preedicted labels to a csv file
    y_pred = predicted
    predicted = model.predict_proba(testdata)
    np.savetxt("svmrbfpred.csv", y_pred)

    count = 0					#initialise count
    y_pred = y_pred.ravel()				#converting arrays of array to 1D array
    y_pred = y_pred.tolist()			#converting array to a list
    count = y_pred.count(1)				#finding the count of 1 s in given list
    hours = len(y_pred)/60				#finding the total number of hours
    AHI = count/hours
    print "AHI IS :" , AHI
    return AHI

