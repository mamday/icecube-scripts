#!/usr/bin/env python
from os.path import expandvars
import math,sys
import collections
import numpy

import icecube
from icecube import icetray, dataclasses, dataio, phys_services,simclasses
from icecube.icetray import I3Tray
from I3Tray import *


tray = I3Tray()

geofile = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]
omKey3Vec_ = []
omKey4Vec_ = []
omKey5Vec_ = []
omKey6Vec_ = []

gcdfile = dataio.I3File(geofile)

geo_frame = gcdfile.pop_frame()
while not geo_frame.Has('I3Geometry'): geo_frame = gcdfile.pop_frame()
geometry_ = geo_frame.Get('I3Geometry')


def GetCore(frame):
#  global omKey3Vec_, omKey4Vec_, omKey5Vec_, omKey6Vec_
#  omKey3Vec_ = []
#  omKey4Vec_ = []
#  omKey5Vec_ = []
#  omKey6Vec_ = []
  if(frame.Has("OfflinePulses_sRT")):
    srtMask = frame["OfflinePulses_sRT"]
    srtPulse = srtMask.apply(frame)
    pulseList = []
    firstStrings = []
#Store srtPulse information in a  list of tuples with time variable first
    for omKey, series in srtPulse:
      pulseTup = series[0].time, omKey.string, omKey, geometry_.omgeo[omKey].position[2] 
      pulseList.append(pulseTup)
#Get number of hits on each string
    stringList = [i[1] for i in sorted(pulseList)]
    stringCount = [stringList.count(j) for j in stringList]
#Make pulseList sorted in Time
    pulseList.sort()
    frame["ThreePosX"] = dataclasses.I3Double(geometry_.omgeo[[i for i,j in srtPulse][stringCount.index(min([i for i in stringCount if i>2]))]].position[0])
    frame["ThreePosY"] = dataclasses.I3Double(geometry_.omgeo[[i for i,j in srtPulse][stringCount.index(min([i for i in stringCount if i>2]))]].position[1])
    frame["ThreePosZ"] = dataclasses.I3Double(geometry_.omgeo[[i for i,j in srtPulse][stringCount.index(min([i for i in stringCount if i>2]))]].position[2])
#    print dataclasses.I3Double(geometry_.omgeo[[i for i,j in srtPulse][stringCount.index(min([i for i in stringCount if i>2]))]].position[1]),dataclasses.I3Double(geometry_.omgeo[[i for i,j in srtPulse][stringCount.index(min([i for i in stringCount if i>2]))]].position[2])
#Save strings with >2 hits in time order
#    firstStrings = [] 
#    for i in xrange(len(pulseList)):
#      if(stringCount[i]>2 and not(pulseList[i][1] in firstStrings)):
#        firstStrings.append(pulseList[i][1])

#Make lists of omkeys for first 3,4,5 and 6 strings in event with >2 hits
#    countHits = 87*[0] 
#    for tup in xrange(len(pulseList)):
#      countHits[stringList[tup]]+=1
#      if(stringCount[tup]>2):
#        if(countHits[stringList[tup]]<=round(.68*stringCount[tup])):
#          if(stringList[tup] in firstStrings[:3]):
#            omKey3Vec_.append(pulseList[tup][2])  
#          if(stringList[tup] in firstStrings[:4]):
#            omKey4Vec_.append(pulseList[tup][2])  
#          if(stringList[tup] in firstStrings[:5]):
#            omKey5Vec_.append(pulseList[tup][2])  
#          if(stringList[tup] in firstStrings[:6]):
#            omKey6Vec_.append(pulseList[tup][2])  

#Really dumb algorithms to select Pulses
def selector3(omkey,index,pulse):
  truthBool = False
  for k in xrange(len(omKey3Vec_)):
    if(omkey==omKey3Vec_[k]):
      truthBool = True
      break
    else:
      truthBool = False
  if(truthBool):
    return truthBool

def selector4(omkey,index,pulse):
  truthBool = False
  for k in xrange(len(omKey4Vec_)):
    if(omkey==omKey4Vec_[k]):
      truthBool = True
      break
    else:
      truthBool = False
  if(truthBool):
    return truthBool

def selector5(omkey,index,pulse):
  truthBool = False
  for k in xrange(len(omKey5Vec_)):
    if(omkey==omKey5Vec_[k]):
      truthBool = True
      break
    else:
      truthBool = False
  if(truthBool):
    return truthBool

def selector6(omkey,index,pulse):
  truthBool = False
  for k in xrange(len(omKey6Vec_)):
    if(omkey==omKey6Vec_[k]):
      truthBool = True
      break
    else:
      truthBool = False
  if(truthBool):
    return truthBool

def MaskPulses(frame):
  frame['String3Pulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses', selector3)
  frame['String4Pulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses', selector4)
  frame['String5Pulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses', selector5)
  frame['String6Pulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses', selector6)

tray.AddModule('I3Reader', 'reader',
               FilenameList = [geofile, infile]
               )

tray.AddModule(GetCore,'test')

#tray.AddModule(MaskPulses,'theMask')

tray.AddModule('I3Writer', 'writer',
    Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics],
####    filename='/net/user/mamday/icesim/scripts/output/JPNuMu/'+outfile)
    filename=outfile)

tray.AddModule('TrashCan', 'trash')
tray.Execute()
tray.Finish()

