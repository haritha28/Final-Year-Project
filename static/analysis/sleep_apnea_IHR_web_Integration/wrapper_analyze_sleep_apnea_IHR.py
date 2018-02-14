'''
Wrapper program to be called from the server to analyze a give 
file (such as a01.ihr.csv) for sleep apnea and corresponding
AHI.

Author  : Rahul Krishnan (rahulkrishnan@am.amrita.edu)
Date    : 3 June 2017
Version : 1
'''
import static.analysis.sleep_apnea_IHR_web_Integration.transpose_ihr as SP
import static.analysis.sleep_apnea_IHR_web_Integration.svm_analyze_ihr as SV
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))

def sendFile(input):
	file_name = input
	print ("Filename is")
	print (file_name)
	out = SP.transpose_ihr(file_name)
	AHI = SV.svm_analyze_ihr(out)
	print ('Apnea Hypoapea Index for the given patient file '),\
	    file_name, ' is ', AHI, '.'
	return AHI
    
    
