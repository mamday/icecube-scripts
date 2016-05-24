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
omKeyC5Vec_ = []
omKeyC6Vec_ = []

gcdfile = dataio.I3File(geofile)

geo_frame = gcdfile.pop_frame()
while not geo_frame.Has('I3Geometry'): geo_frame = gcdfile.pop_frame()
geometry_ = geo_frame.Get('I3Geometry')


def GetCore(frame):
  global omKey3Vec_, omKeyC5Vec_,omKeyC6Vec_
  omKey3Vec_ = []
  omKeyC5Vec_ = []
  omKeyC6Vec_ = []
  if(frame.Has("OfflinePulses_sRT")):
    srtMask = frame["OfflinePulses_sRT"]
   # if(len(srtMask)==0):
   #   return False
# Look at Noise OMKeys
#  if(frame.Has("MCPESeriesMap_withNoise")):
#    mcpePID = frame["MCPESeriesMap_withNoise"]
#    for tKey, tPID in mcpePID:
#      if(tPID[0].major_ID==0):
#        print tKey
    truePart = frame["I3MCTree"].most_energetic_muon
  #  if(truePart):
  #    print truePart.pos[0],truePart.pos[1],truePart.pos[2]
    srtPulse = srtMask.apply(frame)
  #  srtPulse = srtMask
    pulseList = []
    firstStrings = []
#Store srtPulse information in a  list of tuples with time variable first
    totCharge = 0
    for omKey, series in srtPulse:
      if(len(series)==0):
        continue 
      pulseTup = series[0].time, omKey.string, omKey, geometry_.omgeo[omKey].position[2],series[0].charge 
      totCharge+=series[0].charge
      pulseList.append(pulseTup)
#Get number of hits on each string
    stringList = [i[1] for i in sorted(pulseList)]
    stringCount = [stringList.count(j) for j in stringList]
#Make pulseList sorted in Time
    pulseList.sort()
#Save strings with >2 hits in time order
    firstStrings = [] 
    for i in xrange(len(pulseList)):
      if(stringCount[i]>2 and not(pulseList[i][1] in firstStrings)):
        firstStrings.append(pulseList[i][1])

#Make lists of omkeys for first 3,4,5 and 6 strings in event with >2 hits
    countHits = 87*[0] 
    
    #print 'Hi'
    for tup in xrange(len(pulseList)):
      #print 'Time'
     # if(pulseList[tup][4]>1.4):
    #  print pulseList[tup][0],geometry_.omgeo[pulseList[tup][2]].position,pulseList[tup][4]
      #print pulseList
      countHits[stringList[tup]]+=1
      if(stringCount[tup]>2):
        if(countHits[stringList[tup]]<=round(.68*stringCount[tup])):
          if(stringList[tup] in firstStrings[:3]):
            omKey3Vec_.append(pulseList[tup][2])  
    pulseList.sort(key=lambda pulse: pulse[4],reverse=True)
    sortCharge = 0
    for tup in xrange(len(pulseList)):
      if(sortCharge<0.5*totCharge):
        #print '5',pulseList[tup][4],sortCharge,totCharge
        sortCharge+=pulseList[tup][4]
        omKeyC5Vec_.append(pulseList[tup][2])
        omKeyC6Vec_.append(pulseList[tup][2])
      elif (sortCharge>=0.5*totCharge and sortCharge<0.66*totCharge):
        #print '6',pulseList[tup][4],sortCharge,totCharge
        sortCharge+=pulseList[tup][4]
        omKeyC6Vec_.append(pulseList[tup][2])
      else:
        break
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

def selectorC5(omkey,index,pulse):
  truthBool = False
  for k in xrange(len(omKeyC5Vec_)):
    if(omkey==omKeyC5Vec_[k]):
      truthBool = True
      break
    else:
      truthBool = False
  if(truthBool):
    return truthBool

def selectorC6(omkey,index,pulse):
  truthBool = False
  for k in xrange(len(omKeyC6Vec_)):
    if(omkey==omKeyC6Vec_[k]):
      truthBool = True
      break
    else:
      truthBool = False
  if(truthBool):
    return truthBool

def MaskPulses(frame):
  frame['String3Pulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses_sRT', selector3)
  frame['StringC5Pulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses_sRT', selectorC5)
  frame['StringC6Pulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses_sRT', selectorC6)

tray.AddModule('I3Reader', 'reader',
               FilenameList = [geofile, infile]
               )

tray.AddModule(GetCore,'test')

tray.AddModule(MaskPulses,'theMask')

tray.AddModule('I3Writer', 'writer',
    Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics],
    filename='/net/user/mamday/icesim/scripts/output/JPNuMu/'+outfile)

tray.AddModule('TrashCan', 'trash')
tray.Execute()
tray.Finish()

