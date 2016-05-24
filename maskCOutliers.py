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
#Lazy for using OfflinePulses
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
#Lazy for using OfflinePulses
  #  srtPulse = srtMask

#Store srtPulse information in a  list of tuples with time variable first
    pulseList = []
    firstStrings = []
    totCharge = 0
    stringDict = {}
    for omKey, series in srtPulse:
      if(len(series)==0):
        continue 
      domUWCharge = numpy.sum([pulse.charge for pulse in series])
      domCharge = 0 
      domTime = 0 
      chargeHold=0
      sBool = False
      pBool = False
      omPList = [(p.time,p.charge,p.flags) for p in series]
      pickList = [False]*len(omPList)
      #print 'Pulse',pickList,omPList,dataclasses.I3RecoPulse.PulseFlags.ATWD,len(omPList)
#Someday this loop should be a function, when I am less lazy
      for pulse in xrange(len(omPList)):
        if(pickList[pulse]):
          continue
#Only one pulse, keep that time and charge
        if(len(omPList)==1):
          domCharge=round(omPList[pulse][1])
          domTime=omPList[pulse][1]*omPList[pulse][0]
          pickList[pulse]=True
          #print '1',pulse,domCharge,omPList[pulse][1]
        else:
#ATWD
          if(omPList[pulse][2] & dataclasses.I3RecoPulse.PulseFlags.ATWD):
            if(omPList[pulse][1]<0.5):
#Add low charge (charge<0.5) hits to closest hit in time. Prevent collisons (two low charge hits trying to combine with the same hit)
              if((pulse<(len(omPList)-1) and pulse>0 and numpy.fabs(omPList[pulse+1][0]-omPList[pulse][0])<numpy.fabs(omPList[pulse-1][0]-omPList[pulse][0])) or pulse==0):
#Prevent Collisions
                if(pickList[pulse+1]):
                  if(pulse==0 or pickList[pulse-1]):
                    continue
                  else:
                    pickList[pulse]=True
                    pickList[pulse-1]=True
                    domTime+=(omPList[pulse][1]+omPList[pulse-1][1])*omPList[pulse][0]
                    domCharge+=round(omPList[pulse][1]+omPList[pulse-1][1])
                    #print 'Next Col',pulse,domCharge,omPList[pulse][1]
                    continue
#Merge Hits
                pickList[pulse]=True 
                pickList[pulse+1]=True 
                domTime+=(omPList[pulse][1]+omPList[pulse+1][1])*omPList[pulse][0]
                domCharge+=round(omPList[pulse][1]+omPList[pulse+1][1])
                #print 'Next',pulse,domCharge,omPList[pulse][1]
              elif((pulse<(len(omPList)-1) and pulse>0 and numpy.fabs(omPList[pulse+1][0]-omPList[pulse][0])>=numpy.fabs(omPList[pulse-1][0]-omPList[pulse][0])) or pulse==(len(omPList)-1)):
#Prevent Collisions
                if(pickList[pulse-1]):
                  if(pulse==(len(omPList)-1) or pickList[pulse+1]):
                    continue
                  else:
                    pickList[pulse]=True
                    pickList[pulse+1]=True
                    domTime+=(omPList[pulse][1]+omPList[pulse+1][1])*omPList[pulse][0]
                    domCharge+=round(omPList[pulse][1]+omPList[pulse+1][1])
                    #print 'Prev Col',pulse,domCharge,omPList[pulse][1]
                    continue
#Merge Hits
                pickList[pulse]=True 
                pickList[pulse-1]=True 
                domTime+=(omPList[pulse][1]+omPList[pulse-1][1])*omPList[pulse-1][0]
                domCharge+=round(omPList[pulse][1]+omPList[pulse-1][1])
                #print 'Prev',pulse,domCharge,omPList[pulse][1]
#fADC, split sometimes for no apparent reason, keep earliest time, total fADC charge
#TODO: Have a bug here where an ATWD pulse can choose an fADC pulse and the fADC pulse gets added twice
          else:
            domTime=omPList[pulse][0]   
            for e in xrange(len(omPList[pulse:])):
              chargeHold+=omPList[pulse+e][1]
              pickList[pulse+e]=True
            domCharge=round(chargeHold)
            #print 'fADC',pulse,omPList[pulse],domCharge
            break
      #print pickList
#Add anything that didn't get merged
      for u in xrange(len(omPList)):
        if(not(pickList[u])):
          domCharge+=round(omPList[u][1])
          domTime+=omPList[u][1]*omPList[u][0]
#          print 'No Match',u,domCharge,omPList[u][1]

      if(domCharge==0):
        continue
      domTime=domTime/domUWCharge
#      print 'Final:',domCharge,domUWCharge,domTime
#Now make the tuple
      pulseTup = domTime, omKey.string, omKey, geometry_.omgeo[omKey].position[2],domCharge 
      if(not(omKey.string in stringDict)):
        stringDict[omKey.string]=0
      stringDict[omKey.string]+=domCharge
      totCharge+=domCharge
      pulseList.append(pulseTup)
#Get number of hits on each string
    stringList = [i[1] for i in sorted(pulseList)]
    stringCount = [stringList.count(j) for j in stringList]
#Make pulseList sorted in Time
    pulseList.sort()
#Save strings with >2 hits in time order
    firstStrings = [] 
    for i in xrange(len(pulseList)):
      if(stringDict[pulseList[i][1]]>2 and not(pulseList[i][1] in firstStrings)):
        firstStrings.append(pulseList[i][1])

#Make lists of omkeys for first 3 strings in event with >2 charge
    countHits = 87*[0] 
    
    #print 'Hi'
    for tup in xrange(len(pulseList)):
      countHits[stringList[tup]]+=1
      if(stringDict[stringList[tup]]>2):
        if(countHits[stringList[tup]]<=round(.68*stringDict[stringList[tup]])):
          #print stringDict,countHits[stringList[tup]],.68*stringDict[stringList[tup]],stringList[tup],firstStrings[:3]
          if(stringList[tup] in firstStrings[:3]):
           # print 'Select',pulseList[tup][2],pulseList[tup][0],countHits[stringList[tup]],.68*stringDict[stringList[tup]],stringList[tup],firstStrings[:3]
            omKey3Vec_.append(pulseList[tup][2])  
#Make list of omkeys with 50% and 66% of charge
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
#Really dumb algorithms to select Pulses, should be a class probably...
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
  frame['StringCPulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses_sRT', selector3)
  frame['StringC5Pulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses_sRT', selectorC5)
  frame['StringC6Pulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses_sRT', selectorC6)

tray.AddModule('I3Reader', 'reader',
               FilenameList = [geofile, infile]
               )

tray.AddModule(GetCore,'test')

tray.AddModule(MaskPulses,'theMask')

tray.AddModule('I3Writer', 'writer',
    Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics],
    filename='/data/user/mamday/icesim/scripts/output/JPNuE/'+outfile)

tray.AddModule('TrashCan', 'trash')
tray.Execute()
tray.Finish()

