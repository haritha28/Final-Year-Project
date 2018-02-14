README
Author  : Dhara Prathap (dharanair93@gmail.com)
Date    : 3 June 2017

Files in this folder
====================
1. transpose_ihr.py
Use this python code to transpose row-wise arranged IHR values from files ../Dataset/individual_dataset/IHR/..... (including a01.ihr.csv till c10.ihr.csv) and it will also create a csv file for transposed ihr values of length 30
2. svm_create_model.py
Use this python code to create a svm model for training and testing the data. This will save the model as svm-model-1.pkl. Here both training and testing can be done
3. svm_analyse_ihr.py
Use this python code to predict/detect sleep apnea with AHI score from files. Input of this code is the output of transpose.py