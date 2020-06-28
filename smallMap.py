#!/usr/bin/env python


import os
import sys
import optparse
import time
import datetime

if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
     print("SUMO_HOME detected!")
else:
     sys.exit("please declare environment variable 'SUMO_HOME'")


import traci
import simpla
import _utils2
import _platoonmanager2
from xml.etree import ElementTree

# add command line option for not using gui interface (faster simulation runs)
def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False, help="run the command line version of SUMO")
    options, args = opt_parser.parse_args()
    return options

# TraCI control loop
def run():
    step = 0

    # todo Write VMT + status info to file
    #  walk through pvehicles for each time step
    #  time step | pvehicle | vehicle type | getDistance
    #  make xml
    #  <time step>
    #      <pevehicle id | type | distance />
    #  </time step>

    now = datetime.datetime.now()
    log = now.strftime("%Y-%m-%d-%H-%M-%S") + "platoon_status.xml"
    file = '/home/thomasrw/Desktop/' + log

    #root = ElementTree.fromstring('<platoon_status>\n</platoon_status>')
    #tree = ElementTree.ElementTree(root)
    #tree.write(file)

    logfile = open(file, 'w')
    logfile.write('<platoon_status>\n')

    tree = ''

    #while step < 41000:
    while traci.simulation.getMinExpectedNumber() > 0:
        #if step == 100:
            #simpla._utils.openGap("flow20.0", 1, 1, 1, 1)
            #sr = _utils2.SizeRestrictor(mgr,3,60)
            #listenerID = traci.addStepListener(sr)

        #tree = None
        #if tree == None:
        #    print("reading file")
        #    tree = ElementTree.parse(file)
        #    print("read file complete")
        #    root = tree.getroot()
        #timestep = ElementTree.SubElement(root, 'time')
        #timestep.set('value', str(step))
        #timestep.tail = "\n"

        tree += '<time value="' + str(step) + '">\n'


        for veh_id in traci.vehicle.getIDList():
            distance = traci.vehicle.getDistance(veh_id)
            type = traci.vehicle.getTypeID(veh_id)

            #status = ElementTree.SubElement(timestep, 'vehicle')
            #status.set('id', str(veh_id))
            #status.set('distance', str(distance))
            #status.set('type', str(type))
            #status.tail="\n"

            tree += '<vehicle id="'+str(veh_id)+'" distance="'+str(distance)+'" type="'+str(type)+'"/>\n'

            #print(veh_id, distance, type)

        tree += '</time>\n'
        if step % 10000 == 0:  #write to file every 10,000 steps
            logfile.write(tree)
            tree = ''

        traci.simulationStep()
        print(step)
        step += 1

    if tree == '':
        pass #last step was a write step
    else:
        logfile.write(tree) #write final entry from last set of steps

    logfile.write('</platoon_status>')
    logfile.close()
    traci.close()
    sys.stdout.flush()






# main entry point
if __name__ == "__main__":
    options = get_options()
    if options.nogui:
        sumoBinary = "/usr/share/sumo/bin/sumo"
    else:
        sumoBinary = "/usr/share/sumo/bin/sumo-gui"

    # passing the "--start" option to tell sumo-gui to begin without waiting for the play button to be pressed
    sumoCmd = [sumoBinary, "-c", "/home/thomasrw/j/jconfig", "--start"]
    simplaConfig = "/home/thomasrw/j/mysimpla.cfg.xml"
    #simplaConfig2 = "/home/thomasrw/Model/mysimpla2.cfg.xml"

    traci.start(sumoCmd)
    #simpla.load(simplaConfig)

    #calling config.load() and platoonmanger() explicitly exposes the platoon manager variable allowing listeners
    #  to be specified by platoon manager

    simpla._config.load(simplaConfig)
    ##mgr = simpla._platoonmanager.PlatoonManager()
    mgr = _platoonmanager2.PlatoonManager2()
    mgr_id = traci.addStepListener(mgr)

    #print(str(mgr.getMaxSize()))
    #mgr.setMaxSize(50)
    #print(str(mgr.getMaxSize()))

    #simpla.load(simplaConfig2)

    start = time.time()
    run()
    end = time.time()
    total = end - start
    print("time taken is: " + str(total))
