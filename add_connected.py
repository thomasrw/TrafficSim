
from xml.etree import ElementTree
import os.path
from os import path
import sys
import random

number = sys.argv[1]
#mypercent = sys.argv[2]



#mypath = '/home/thomasrw/Model/'
mypath = '/work/thoma525/'


def format(target, percent):
    tree =ElementTree.parse(target)
    root = tree.getroot()
    #root.tag = "additional"
    #root.attrib = None
    #for att in root:
    #    att.set('departSpeed', 'max')
    b = ElementTree.SubElement(root, 'vType')
    b.set('id', 'CAV_VEHTYPE')
    b.tail = '\n'

    # sort so vtypes come first. vtypes must be defined before vehicles that use them
    root[:] = sorted(root, key=lambda child: (child.tag,child.get('name')))

    for att in root:
        if att.tag == 'vehicle':
            if random.randrange(100) + 1 <= int(percent):
                #change type to connected type specified in mysimpla.cfg.xml
                att.set('type', 'CAV_VEHTYPE')
                #add discriminator for joining strategy when using adhoc platoon game based on %results
                #from paper:
                #Cooperator 22% [1-22]
                #Defector 16% [23-38]
                #TitForTat 23% [39-61]
                #Grudger 23% [62-84]
                #Random(0.5) 16% [85-100]

                pick = random.randrange(100) + 1 #needs new rand to that full range of strategy considered
                if pick <= 22:
                    id = att.get('id')
                    id = 'coop' + id
                    att.set('id', id)

                elif pick <=38: #<=22 would have already been selected if true
                    id = att.get('id')
                    id = 'def' + id
                    att.set('id', id)
                elif pick <= 61:
                    id = att.get('id')
                    id = 'tft' + id
                    att.set('id', id)
                elif pick <= 84:
                    id = att.get('id')
                    id = 'grud' + id
                    att.set('id', id)
                else:
                    id = att.get('id')
                    id = 'rand' + id
                    att.set('id', id)

    #todo clean so not dependent on sys.argv[1] (number)
    myfile = mypath + "CAV" + str(percent).zfill(3) + '_' + str(number)
    tree.write(myfile)




mytarget = mypath + "CAV000" + '_' + str(number)
#format(mytarget, mypercent)

for i in range(100):
    format(mytarget, i+1)
    print(str(i) + " complete")

print("success for " + mytarget)



