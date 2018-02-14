README
Author  : Durga P (durga.amr@gmail.com)
Date    : 5 June 2017

Files in this folder
====================
1.svm_train_AHE_prediction_model.py : 
	This code creates the model for prediction of AHE in patients using the file 
	"h1-h2-c1-180-ms-before-svm-training.csv".
	"svm-model-0.pkl" is the model thus created.

2. svm_analyze_AHE.py
	Use this code to predict future occurrence of AHE in patients, using abp data of the patient.

3. wrapper_analyze_AHE_abp
	This code calls the function svm_analyze_AHE to predict occurrence of AHE in patients.
