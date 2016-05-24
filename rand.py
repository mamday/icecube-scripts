#!/usr/bin/env python

import icecube
from icecube import dataio, dataclasses, phys_services, icetray
from I3Tray import *
import sys
import numpy
import math

gcdfile = sys.argv[1]
outfile = sys.argv[2]
infiles = sys.argv[3:]

inputfiles = [gcdfile] 
for i in xrange(100):
  for file1 in infiles:
    inputfiles.append(file1)

fileInd = 0

myR = phys_services.I3GSLRandomService(80000)
randInd = []
for i in xrange(30):
  randInd.append(myR.integer(40000)) 
  randInd.sort()


def ChooseRand(frame):
  global fileInd
  truthBool = False 
  if (frame.Has('OfflinePulses_sRT')):
    for i in xrange(len(randInd)):
      if(fileInd)==randInd[i]:
        truthBool = True
        break
      else:
        truthBool = False
    fileInd+=1
#    print fileInd, randInd[0:5]
    return truthBool 

tray = I3Tray()

tray.AddModule('I3Reader', 'reader', FilenameList=inputfiles)

tray.AddModule(ChooseRand,'myRand')

tray.AddModule('I3Writer', 'writer',
Filename=outfile,
DropOrphanStreams=[icetray.I3Frame.DAQ],
Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics])

tray.AddModule('TrashCan','can')
tray.Execute()
tray.Finish()
