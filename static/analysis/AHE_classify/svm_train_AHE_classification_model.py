# Date: 18-01-2017
# Progarm to train and test SVM classifier for AHE.
# Modified to include SVM grid search functionality too.

from __future__ import print_function

from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

import numpy as np
import pandas as pd
from sklearn.externals import joblib

print(__doc__)


inputFileName = "h1-h2-c1-60-min-after-to-svm-training.csv"

dataset = pd.read_csv(inputFileName)

dataset = np.array(dataset)

X = dataset[:, 1:60]   # data 
y = dataset[:, 0]   # annotations

# reshape the data matrix, since there is only 1 feature
#X = X.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

#print X_train.shape
#print X_test.shape
#print y_train.shape
#print y_test.shape

# Set the parameters for grid search
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}]

#tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10]}]

scores = ['precision', 'recall']
i = 0

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(SVC(C=1, probability=True), tuned_parameters, cv=5, n_jobs=-1, scoring='%s_macro' % score)
    clf.fit(X_train, y_train)

    # store the model
    modelName = 'svm-model-%d.pkl' % (i)
    joblib.dump(clf, modelName)
    i = i + 1
    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print(clf.grid_scores_)
    
    #means = clf.cv_results_['mean_test_score']
    #stds = clf.cv_results_['std_test_score']
    #for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        #print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
    #print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))
    print()
    
# store the model
#joblib.dump(clf, 'svm-model-1.pkl') 

# once model is stored, then retrieve it
#clf = joblib.load('trained-model/svm-model-1.pkl') 

#print clf
