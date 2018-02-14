import random
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def sendFile(input):
    file_name = input
    print ("Filename is")
    print (file_name)
    BP = random.randint(50,90)
    print ('Blood Pressure '), \
        file_name, ' is ', BP, '.'
    return BP
