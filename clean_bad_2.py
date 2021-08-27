#Check for incomplete tripinfo files and remove associated files



from xml.etree import ElementTree
import os.path
#from os import path
import os
import sys

#mypath = '/home/thomasrw/Desktop/'
mypath = '/work/thoma525/'

#myPrefix = 'CAV025_100'
myPrefix = 'CAV'

def clean(clean_path=mypath, clean_prefix=myPrefix):
    folder = clean_path + clean_prefix
    try:
        os.remove(folder + '_tripinfo')
        os.remove(folder + '_platoon_status.xml')
        os.remove(folder + '_validation_dets.xml')
        print('cleaned up: ' + folder)
    except:
        print('problem trying to clean')


def check(check_path=mypath, check_prefix=myPrefix):
    folder = check_path + check_prefix
    input = folder + '_tripinfo'

    try:
        tree = ElementTree.parse(input)
        print(input + ' is clean')
    except:
        print('error reading ' + input + ', attempting to clean...')
        clean(check_path, check_prefix)




#check()

for i in range(100):
    myfile = myPrefix + str(i+1).zfill(3) + '_2'
    check(mypath, myfile)
    
