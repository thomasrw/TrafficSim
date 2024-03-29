
from xml.etree import ElementTree
import os.path
from os import path
import sys


number = sys.argv[2]
percent = sys.argv[1]


#mypath = '/home/thomasrw/Model/'
#mypath = '/home/thomasrw/Desktop/'
mypath = '/work/thoma525/'


def format(target):
    tree =ElementTree.parse(target)
    root = tree.getroot()
    root.tag = "additional"
    root.attrib = None
    for att in root:
        att.set('departSpeed', 'max')
    b = ElementTree.SubElement(root, 'vType')
    b.set('color', 'green')
    b.set('id', 'PLATOON_VEHTYPE')
    b.set('tau', '0.1')
    b.tail = '\n'

    c = ElementTree.SubElement(root, 'vType')
    c.set('color', 'blue')
    c.set('id', 'LEADER_VEHTYPE')
    c.set('speedDev', '0')
    c.tail = '\n'



    tree.write(target)

def addCatchup(target):
    tree = ElementTree.parse(target)
    root = tree.getroot()

    c = ElementTree.SubElement(root, 'vType')
    c.set('color', 'red')
    c.set('id', 'CATCHUP_VEHTYPE')
    c.set('speedDev', '0')
    c.set('tau', '0.1')
    c.tail = '\n'

    # sort so vtypes come first. vtypes must be defined before vehicles that use them
    root[:] = sorted(root, key=lambda child: (child.tag, child.get('name')))
    tree.write(target)

def fixExtra(target):
    tree = ElementTree.parse(target)
    root = tree.getroot()

    flag = False
    for vType in root.findall('vType'):
        type = vType.get('id')
        if type == 'CATCHUP_VEHTYPE':
            if flag:
                root.remove(vType)
                print('found duplicate CATCHUP, removing element')
            else:
                flag = True
                print('found 1st CATCHUP, setting flag to true')
    #modTarget = target  + '_new'
    tree.write(target)

#mytarget = mypath + "CAV000" + '_' + str(number)
mytarget = mypath + "CAV" + str(percent) + '_' + str(number)

#format(mytarget)
#addCatchup(mytarget)

fixExtra(mytarget)

