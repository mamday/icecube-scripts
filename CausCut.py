#1/usr/bin/env python

import icecube
from icecube import icetray, common_variables, PulseCore, dataio, dataclasses, phys_services

import numpy, math

from I3CutL7Module import *

from I3Tray import *

geofile = dataio.I3File(sys.argv[1])
gFrame = geofile.pop_frame()
gFrame = geofile.pop_frame()

geometry_ = gFrame["I3Geometry"]

def PCVertCut(frame):
  if(frame.Has("String1Pulses")):
    cogPos = common_variables.hit_statistics.calculate_cog(geometry_,frame["String1Pulses"].apply(frame))
    cut_diff = cogPos - dataclasses.I3Position(29.3,52.6,cogPos.z)
    cut_diff_mag = cut_diff.magnitude
    if(cut_diff_mag<180 and cogPos.z>-500 and cogPos.z<-180):
      return True
    else:
      return False
  else:
    return False


def myCOG(s3Time):
  string3X = 0
  string3Y = 0
  string3Z = 0
  string3T = 0
  totCharge = 0
  for i in xrange(len(s3Time)):
    string3X += s3Time[i][1]*s3Time[i][2][0]
    string3Y += s3Time[i][1]*s3Time[i][2][1]
    string3Z += s3Time[i][1]*s3Time[i][2][2]
    string3T += s3Time[i][1]*s3Time[i][0]
    totCharge += s3Time[i][1]
  return dataclasses.I3Position(string3X/totCharge,string3Y/totCharge,string3Z/totCharge),string3T/totCharge


def mightBeBackground(distance, timeDiff):
    if distance < 750:
        if timeDiff > -5*distance + 500:
            if timeDiff < distance/0.3 + 150:
                if timeDiff > distance/0.3 - 1850:
                    return True
    return False

def MyCausVetCut(frame):
  if(frame.Has("String1Pulses")):
    s3Time = [(p.time,p.charge,geometry_.omgeo[i].position,i.string) for i,j in frame["String1Pulses"].apply(frame) for p in j]
    s3Time.sort()
    mcogPos,mcogT = myCOG(s3Time)
#    trigTime = 0
 #   for trigger in frame["I3TriggerHierarchy"]:
 #     trigKey = trigger.key.config_id
 #     if trigKey==1011:
 #       trigTime = trigger.time
 #       mcogT = trigger.time
 #     for om, launchSeries in frame["InIceRawData"]:
 #         for launch in launchSeries:
 #             hitTime = launch.time
 #             if hitTime==trigTime:
 #                 refHitTime = hitTime
 #                 mcogPos = geometry_.omgeo[om].position

    nVetoHits=0
    for om, launchSeries in frame["InIceRawData"]:
      for launch in launchSeries:
        hitTime = launch.time
        hitPos = geometry_.omgeo[om].position
        hitDistance = (hitPos-mcogPos).magnitude
        hitTimeDiff = mcogT-hitTime

        if mightBeBackground(hitDistance, hitTimeDiff):
          nVetoHits+=1

    if(nVetoHits<=2):
      return True
    else:
      return False
  return False

tray = I3Tray()

tray.Add("I3Reader",FilenameList = [sys.argv[1]])

tray.Add(PCVertCut)

#tray.AddModule(I3CutL7Module, 'cutL7',
#               maxNVetoHits = 2
#               )

tray.Add(MyCausVetCut)

tray.Add("I3Writer",
  DropOrphanStreams = [icetray.I3Frame.DAQ],
  filename='/data/user/mamday/icesim/scripts/output/CutNuMu/'+sys.argv[2])

tray.Execute()
