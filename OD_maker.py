 #Copyright (c) 2020 Robert Thomas

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# @file     OD_maker.py
# @author   Robert Thomas
# @date     2020-06-05


#Todo add citation
'''
Build an O-D Matrix for a Sumo Network from vehicle routes using the entropy maximizing approach in CITATION.
Build an emitter files for Sumo specifying flows to match the generated matrix
'''

#Read Routes.xml
#Build O-D pair dict() of {Route : [bool, edge 0, edge 1, ... ,edge n]}
#Build Link count dict() of {Edge : Count}
#Build Link constraint dict() {Edge: Count_Constraint}
#Implement alg steps
#Todo build emmitter flows

from xml.etree import ElementTree
import random
import math
import time

#input = '/home/thomasrw/j/myOUT-route.xml'
#constraints = '/home/thomasrw/j/constraints.xml'

#input = '/home/thomasrw/j/test_route.xml'
#constraints = '/home/thomasrw/j/test_constraints.xml'

input = '/home/thomasrw/Model/myOUT-route.xml'
constraints = '/home/thomasrw/Model/mape_constraints.xml'



class OD_Maker():

    _blank = dict()
    def __init__(self, routes, constraints):
        self._ODpairs = dict()
        self._linkCounts = dict()
        self._linkConstraints = dict()
        #self._blank = dict()

        self._build_ODpairs(routes)
        self._build_linkCounts()
        self._build_linkConstraints(constraints)
        self._constraintPriority = self._prioritize_constraints()



    def _build_ODpairs(self, routes):
        '''
        Build an O-D pair dict() of {Route : [bool, edge 0, edge 1, ... ,edge n]} from a Sumo routes.xml file
        bool (0 or 1) indicates if the O-D pair is 0=open or 1=closed when generating the O-D matrix

        :param routes:
        :return:
        '''
        tree = ElementTree.parse(routes)
        root = tree.getroot()

        for att in root:
            key = att.attrib['id']
            value = att.attrib['edges']
            list = value.split()
            list.insert(0,0) #insert 0 at index 0 to indicate that the O-D pair is "open"
            self._ODpairs[key] = list

    def _prioritize_constraints(self):
        '''
        Sort contraint-links based on which has the most preceeding links in the network
        :return: links[]
        '''

        priority = dict()
        for link in self._linkConstraints:
            max = 0
            for od in self._ODpairs:
                if link in self._ODpairs[od] and self._ODpairs[od].index(link) > max:
                    max = self._ODpairs[od].index(link)
            priority[link] = max

        topConstraint = sorted(priority.items(), key=lambda x: x[1], reverse=True)
        return topConstraint

    def _build_linkCounts(self):
        '''
        Build link counts dict() from ODpairs, initialized to 0
        :return:
        '''
        for key in self._ODpairs:
            list = self._ODpairs[key]
            length = len(list)
            for val in range(1, length):
                self._linkCounts[list[val]] = 0

    def _find_ODpairs_by_link(self, link):
        '''
        Return list of keys for ODpairs that contain link
        :param link:
        :return: keys[]
        '''
        ods = []
        for od in self._ODpairs:
            list = self._ODpairs[od]
            if link in list:
                ods.append(od)
        return ods


    def _increment_links(self, OD_Key, n=1):
        '''
        Increment links used by the given OD_Pair
        :param OD_Key: int n for amount to increment
        :return:
        '''
        list = self._ODpairs[OD_Key]
        length = len(list)
        for val in range(1, length):
            self._linkCounts[list[val]] += n


    def _build_linkConstraints(self, constraints):
        '''
        Build link constraints dict() from Sumo "additional" style xml file
        Example:
        <?xml version="1.0" encoding="UTF-8"?>
        <additional>
            <polling_station  id="0071_E" count="3196" edge=" 28981762" begin="0" end="3600" />
            <polling_station  id="0071_W" count="1016" edge=" 265151576" begin="0" end="3600" />

            <polling_station  id="0124_E" count="898" edge=" 30199406#0" begin="0" end="3600" />
            <polling_station  id="0124_W" count="1989" edge=" 30199404#1" begin="0" end="3600" />
        </additional>

        Currently only supports count for constraint. Future versions should support time windows.

        :return:
        '''
        tree = ElementTree.parse(constraints)
        root = tree.getroot()

        for att in root:
            key = att.attrib['edge']
            value = att.attrib['count']
            self._linkConstraints[key] = value

    def _OD_Open(self):
        '''
        Check to see if at least one _ODpairs is open (_ODpairs[key][0] == 0)
        :return: Bool
        '''

        #for key in self._ODpairs:
        #    if self._ODpairs[key][0] == 0:
        #        return True
        #return False

        for j in range(len(self._constraintPriority)):
            c_link = self._constraintPriority[j][0]
            # print('clink is: ' + c_link)
            ods = self._find_ODpairs_by_link(c_link)
            for od in ods:
                if self._ODpairs[od][0] == 0:
                    print(c_link)
                    return True
        return False

    def computeOD(self, i=1000, result_input = _blank):
        '''
        Computes O-D matrix i times, returns dict() with key equal to a valid O-D matrix and value equal to the number
        of times that solution was generated within i iterations
        :param i: int number of iterations to run. default 1,000
        :return: dict() O-D pairs (key) with int of vehicles traveling from that O to D (value). the key with the
            highest value is the most common response
        '''
        #todo fix description :return:
        # also return "avg matrix"


        #Alg Step 1
        NTOT = 0 #total number of trials
        solution = dict() #key = result dict() : value = # of occurances as a result

        while NTOT < i:
            print('starting run: ' + str(NTOT))
            #Alg Step 2
            #print('step 2')
            if result_input:
                result = result_input
                print("input: ")
                print(result_input)
            else:
                result = dict()
                print("no input")
                print(result)
            #result = result_input
            print("result is")
            print(result)
            #todo check on link counts
            self._build_linkCounts()
            if result_input:
                for key in result_input:
                    self._increment_links(key, result_input[key])

            for key in self._ODpairs:
                self._ODpairs[key][0] = 0
                if not result_input:
                    result[key] = 0
                    print('building')
            print("built")

            #todo clean this up, repeated code but necessary as currently implemented
            if result_input:
                result = result_input
                print("confirming input taken: ")
                print(result)

            while self._OD_Open():
                print('open')
                print(result)
                #Alg Step 3
                #print('step 3')
                #pair = random.choice(list(self._ODpairs.keys()))
                #fixme forcing order of selection
                '''
                if self._ODpairs["1_to_4"][0] == 0:
                    pair = "1_to_4"
                elif self._ODpairs["1_to_3"][0] == 0:
                    pair = "1_to_3"
                elif self._ODpairs["2_to_4"][0] == 0:
                    pair = "2_to_4"
                else:
                    pair = "2_to_3"
                if self._ODpairs["2_to_4"][0] == 0:
                    pair = random.choice(["1_to_4", "2_to_4"])
                #elif self._ODpairs["1_to_3"][0] == 0:
                #    pair = "1_to_3"
                else:
                    pair = random.choice(list(self._ODpairs.keys()))
                '''
                for j in range(len(self._constraintPriority)):
                    c_link = self._constraintPriority[j][0]
                    #print('clink is: ' + c_link)
                    #fixme 0006S getting boxed in by no offramps before 0007S and 0007S filling first from other routes
                    if "78420935" in self._linkConstraints and int(self._linkConstraints["78420935"]) > self._linkCounts["78420935"]:
                        c_link = "78420935"

                    if int(self._linkConstraints[c_link]) > self._linkCounts[c_link]:
                        #print(random.choice(self._find_ODpairs_by_link(c_link)))
                        l = list()
                        for od in self._find_ODpairs_by_link(c_link):
                            if self._ODpairs[od][0] == 0:
                                l.append(od)
                        print(l)
                        pair = random.choice(l) #pick randomly from open pairs
                        #print(pair)
                        break
                    #    print(pair)
                    #    print('top priority: ' + str(self._constraintPriority[i]))



                #Alg Step 4
                #print('step 4')
                if self._ODpairs[pair][0] == 1:
                    print('closed')
                    continue

                #Alg Step 5
                #print('step 5')
                result[pair] += 1
                self._increment_links(pair)

                #Alg Step 6
                #print('step 6')
                for key in  self._linkConstraints:
                    print("comparing" + self._linkConstraints[key] + " and " + str(self._linkCounts[key]))
                    if self._linkConstraints[key] == str(self._linkCounts[key]):
                        #Alg Step 7 close_pairs_with_link
                        #print('step 7777777')
                        for od in self._ODpairs:
                            if key in self._ODpairs[od]:
                                self._ODpairs[od][0] = 1
                #exiting the while loop when all OD_Pairs are closed is Alg Step 8
            #Alg step 9 check that all constraints are met
            print('step 9')
            for key in self._linkConstraints:
                if int(self._linkConstraints[key]) > self._linkCounts[key]:
                    print('Error: bad results matrix; ' + key + ' link is not saturated')
                    print('scrub results and redo this run')
                    #Alg Step 13
                    NTOT -= 1
                    result = None
                    break


            #Alg step 10 update NTOT and results{}
            print('step 10')
            print(result)
            result_str = str(result)
            if result_str in solution:
                print('repeat')
                solution[result_str] += 1
            else:
                print('new result')
                solution[result_str] = 1
            NTOT += 1
            #result = dict()
            #exiting the for loop when NTOT reaches i is Alg Step 11
        #Alg Step 12 return solution
        return solution

    def buildEmitter(self, od_values, file='/home/thomasrw/Desktop/newEmitterOut.xml'):
        #todo needs a better default file location
        #tree = ElementTree.fromstring('<additional/>')
        root = ElementTree.fromstring('<additional>\n<vType id="DEFAULT_VEHTYPE" speedFactor="normc(1.10,0.10,0.20,2.00)"/>\n<vType id="PLATOON_VEHTYPE" tau="0.1" color="green"/>\n<vType id="LEADER_VEHTYPE" color="blue" speedDev="0"/>\n</additional>')

        #    <flow id="flow1" type="DEFAULT_VEHTYPE" begin="500" end="4099" vehsPerHour="914.795" from="gneE12" to="158140892"/>

        splits = od_values.split(',')
        num_flows = len(splits)
        for i in range(len(splits)):
            pair = splits[i].split(':')
            route = pair[0].strip("{} '")
            route = route.split("_to_")
            origin = route[0]
            destination = route[1]
            count = pair[1].strip("{} '")
            if count == str(0):
                continue #SUMO does not allow emiiter.xml to define flows with vehsPerHour = "0"
            #print(origin, destination)
            #splits[i] = splits[i].strip("{} '")
            flow = ElementTree.SubElement(root, 'flow')
            flow.set('id', str(i))
            flow.set('type', 'DEFAULT_VEHTYPE')
            flow.set('begin', '500')
            flow.set('end', '4099')
            flow.set('vehsPerHour', str(count))
            flow.set('from', str(origin))
            flow.set('to', str(destination))
            flow.set('departLane', "free")
            flow.set('departSpeed', "max")
            flow.tail="\n" #help xml output print in a more readable foramt
        #print(splits)
        #print(len(splits))
        '''
        num = str(100)
        origin = 'a'
        destination = 'b'
        for i in range(num_flows):
            flow = ElementTree.SubElement(root, 'flow')
            flow.set('id', i)
            flow.set('type', 'DEFAULT_VEHTYPE')
            flow.set('begin', '500')
            flow.set('end', '4099')
            flow.set('vehsPerHour', num)
            flow.set('from', origin)
            flow.set('to', destination)
        '''
        print('root is')
        print(root.tag)
        print(root.attrib)
        for child in root:
            print(child.tag, child.attrib)
        #ElementTree.dump(root)
        tree = ElementTree.ElementTree(root)
        tree.write(file)




print("OD maker")

od = OD_Maker(input, constraints)
print(od._ODpairs)
print(od._linkCounts)
print(od._linkConstraints)
#od._ODpairs['gneE14_to_158140892'][0] = 5
#print(od._ODpairs['gneE14_to_158140892'][0])


start = time.time()
myOD = od.computeOD(1)
#for key in od._linkConstraints:
#     print(od._linkConstraints[key] + ' ----- ' + str(od._linkCounts[key]))

topOD = sorted(myOD.items(), key=lambda x: x[1], reverse=False)
for i in topOD:
    print(i[0], i[1])

#print(od._constraintPriority)

print(topOD[0][0])
#splits = topOD[0][0].strip("{} ")

myfile='/home/thomasrw/Desktop/newLargeEmitterOut.xml'
od.buildEmitter(topOD[0][0], myfile)
end = time.time()
total = end - start
print("time taken is: " + str(total))


'''
avgSoln = dict()

for key in myOD:
    key  = key[1:-1]
    list = key.split(',')
    for ele in list:
        newEle = ele.split(':')
        newEle[0] = newEle[0].strip()
        newEle[0] = newEle[0].strip("'")
        newEle[1] = newEle[1].strip()
        newEle[1] = int(newEle[1])
        if newEle[0] in avgSoln:
            avgSoln[newEle[0]] += newEle[1]
        else:
            avgSoln[newEle[0]] = newEle[1]
for key in avgSoln:
    avgSoln[key] = avgSoln[key] / 1000 #divide by i

print("avgSoln is:")
print(avgSoln)

for key in avgSoln:
    avgSoln[key] = math.floor(avgSoln[key])
print("avgSoln floor:")
print(avgSoln)

#od._build_ODpairs(input)
od2 = OD_Maker(input, constraints)

myOD2 = od2.computeOD(1, avgSoln)
print("closest soln to floor avg:")
print(myOD2)

print("done")
'''