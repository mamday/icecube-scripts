#!/usr/bin/env python
from os.path import expandvars
import math,sys

import icecube
from icecube import icetray, dataclasses, dataio, phys_services,simclasses
from icecube.icetray import I3Tray
from I3Tray import *


tray = I3Tray()

geofile = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]
omKeyVec = []

def testFrame(frame):
#  if(frame.Has("I3MCPulseSeriesMapParticleIDMap")):
#    mcpePID = frame["I3MCPulseSeriesMapParticleIDMap"]
  if(frame.Has("MCPESeriesMap_withNoise")):
    mcpePID = frame["MCPESeriesMap_withNoise"]
    for tKey, tPID in mcpePID:
#      for tPID in tPIDVec:
        if(tPID[0].major_ID!=0):
          omKeyVec.append(tKey)
  #print omKeyVec

#Dumb algorithm to count NC and total events
def selector(omkey,index,pulse):
  truthBool = False
  for k in xrange(len(omKeyVec)):
    if(omkey==omKeyVec[k]):
      truthBool = True
      break
    else:
      truthBool = False
  if(truthBool):
    return truthBool



def MaskPulses(frame):

  frame['NoiselessPulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses', selector)

tray.AddModule('I3Reader', 'reader',
               FilenameList = [geofile, infile]
               )

tray.AddModule(testFrame,'test')
tray.AddModule(MaskPulses,'theMask')

tray.AddModule('I3Writer', 'writer',
    Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics],
    filename=outfile)

tray.AddModule('TrashCan', 'trash')
tray.Execute()
tray.Finish()

