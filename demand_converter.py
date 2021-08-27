
from xml.etree import ElementTree
import os.path
from os import path
import sys
import _utils2

prefix = sys.argv[1]

number = int(sys.argv[2])

parallel = False

if len(sys.argv) > 3:
    parallel = sys.argv[3]


#mypath = '/home/thomasrw/Model/'
mypath = '/work/thoma525/'


if parallel:
    print(parallel)
    myinfo = mypath + prefix + '_' + str(number) + '_tripinfo'
    print(myinfo)
    myroutes = mypath + str(number)
    mytarget = mypath + "CAV000" + '_' + str(number)
    _utils2.createDemand(myinfo, myroutes, mytarget)


else:
    for i in range(number):
        myinfo = mypath + prefix +'_' + str(i) + '_tripinfo'
        print(myinfo)
        myroutes = mypath + str(i)
        mytarget = mypath + "CAV000" + '_' + str(i)
        _utils2.createDemand(myinfo, myroutes, mytarget)

