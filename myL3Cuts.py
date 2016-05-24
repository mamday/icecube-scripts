#!/usr/bin/env python

import icecube
from icecube import PulseCore, neutrinoflux, static_twc, SeededRTCleaning, TopologicalSplitter, NoiseEngine, dataclasses, clast, dataio, icetray

#from I3CutL7Module import *

import level3_DeepCore

import numpy, math

from I3Tray import *

geofile = dataio.I3File(sys.argv[2])

gFrame = geofile.pop_frame()
print gFrame.keys()
gFrame = geofile.pop_frame()
print gFrame.keys()
geometry_ = gFrame["I3Geometry"]

sum_weight = 0 
file_num = 0 
evt_holder = 0 
#n_files = 989 
#n_files = 18 
#n_files = 10 
#n_files = 100 
n_files = 1 

flux = neutrinoflux.ConventionalNeutrinoFlux("honda2006_numu")

def noiseWeight(frame):
  global sum_weight
  evt_id = frame["I3EventHeader"].event_id
  weight = (1-(2800*.00003))/(n_files*1000*0.1)
  sum_weight+=weight
  frame["weight"] = dataclasses.I3Double(weight)

def uwcorsikaWeight(frame):
  global sum_weight
  evt_id = frame["I3EventHeader"].event_id
  weight = 1/4.014
  sum_weight+=weight
  frame["weight"] = dataclasses.I3Double(weight)

def FileIter(frame):
  global file_num,evt_holder
  evt_id = frame["I3EventHeader"].event_id
  if (evt_id>evt_holder): 
    evt_holder=evt_id
  else:
    file_num+=1
    evt_holder=0

def MPEZenCut(frame):
  if(frame.Has("MPEFit")):
    if(numpy.cos(frame["MPEFit"].dir.zenith)>0):
      return False
    else:
      return True
  return False

def insert_weight(frame):
    global sum_weight
    if "I3MCTree" and "I3MCWeightDict" in frame:
      tree = frame["I3MCTree"]
      weight_dict = frame["I3MCWeightDict"]
      nu_type = tree.most_energetic_primary.type
      nu_energy = tree.most_energetic_primary.energy
      nu_costheta = math.cos(tree.most_energetic_primary.dir.zenith)
      atmoflux = flux.getFlux(nu_type, nu_energy, nu_costheta)
      weight = 2*weight_dict["OneWeight"]*atmoflux/(n_files*weight_dict["NEvents"])
      sum_weight+=weight
      if not "weight" in frame :
        frame["weight"] = dataclasses.I3Double(weight)

def insert_corsikaweight(frame):
    global sum_weight
    if "CorsikaWeightMap" in frame:
      cMap = frame["CorsikaWeightMap"]
      dipWeight = cMap["DiplopiaWeight"]
      polyWeight = cMap["Polygonato"]
      timeScale = cMap["TimeScale"]
      cWeight = cMap["Weight"]
      sum_weight+=cWeight*polyWeight*dipWeight/(n_files*timeScale)
      if not "weight" in frame :
        frame["weight"] = dataclasses.I3Double(cWeight*polyWeight*dipWeight/(n_files*timeScale))

def mightBeBackground(distance, timeDiff):
    if distance < 750:
        if timeDiff > -5*distance + 500:
            if timeDiff < distance/0.3 + 150:
                if timeDiff > distance/0.3 - 1850:
                    return True
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


def MyCausVetCut(frame):
  if(frame.Has("String1Pulses")):
    s3Time = [(p.time,p.charge,geometry_.omgeo[i].position,i.string) for i,j in frame["String1Pulses"].apply(frame) for p in j]
    s3Time.sort()
    mcogPos,mcogT = myCOG(s3Time) 
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


def FiltCut(frame):
  if(frame.Has("FilterMask")): 
    if(frame["FilterMask"]["DeepCoreFilter_11"].condition_passed):
      return True
    else:
      return False
  else:
    return False 

from icecube import common_variables

def PCVertCut(frame):
  if(not(frame.Has("SRTTWOfflinePulsesDC"))):
    return False
  if(frame.Has("String1Pulses")):
#  if(frame.Has("CLastTWOff_DC")):
#    if(len(frame["String1Pulses"].apply(frame))==0): return False
    cogPos = common_variables.hit_statistics.calculate_cog(geometry_,frame["String1Pulses"].apply(frame)) 
#    cogPos = frame["CLastTWOff_DC"].pos 
    cut_diff = cogPos - dataclasses.I3Position(29.3,52.6,cogPos.z)
    cut_diff_mag = cut_diff.magnitude 
    if(cut_diff_mag<180 and cogPos.z>-500 and cogPos.z<-180):
    #if(cut_diff_mag<150 and cogPos.z<-180):
      return True
    else:
      return False
  else:
    return False

tray = I3Tray()

tray.Add("I3Reader",FilenameList = sys.argv[2:])



####tray.Add(FileIter)

from icecube import common_variables
from icecube.common_variables import hit_statistics
def ZTravelCut(frame):
  if(frame.Has('TWOfflinePulsesDC')):
    tw_dc_pulses = frame['TWOfflinePulsesDC']
    z_travel = hit_statistics.calculate_z_travel(geometry_,tw_dc_pulses.apply(frame))
    if(z_travel.value>-30):
       return True
    else:
      return False

def NEBool(frame):
  if(frame['NoiseEngine_S3bool'].value):
    return True 
  else:
    return False

def MinHitCut(frame):
  if(frame.Has("String1Pulses") and frame.Has("OfflinePulses_sRT")):
    #if((float(len(frame["String1Pulses"].apply(frame)))/float(len(frame["OfflinePulses_sRT"].apply(frame))))>0.33):
#    if(len(frame["String1Pulses"].apply(frame))<2):
    dc_list = [26,27,35,36,37,45,46,79,80,81,82,83,84,85,86]
    charge = 0
    doms = 0
    srtPulses = frame["OfflinePulses_sRT"].apply(frame)
    for i,j in srtPulses:
      if(i.string in dc_list):
        doms+=1
        for k in j:
          charge+=k.charge
#    if(charge<8):
    if(charge<8 or doms<5):
      return False
    else:
      return True
  return False

def FPosCut(frame):
  if(frame.Has("String1Pulses") and frame.Has("OfflinePulses_sRT")):
    srtPulses = frame["OfflinePulses_sRT"].apply(frame)
    srtList = [(p.time,geometry_.omgeo[i].position) for i,j in srtPulses for p in j]
    srtList.sort()
    fPos = srtList[0][1]
    cogPos = common_variables.hit_statistics.calculate_cog(geometry_,frame["String1Pulses"].apply(frame)) 
    posDiff = fPos-cogPos
    #print "First: ",fPos[0],fPos[1],fPos[2],posDiff.magnitude
    if(posDiff.magnitude<50):
      return True
    else:
      return False

def VertDiffCut(frame):
  if(frame.Has("String1Pulses") and frame.Has("CascadeLast_DC")):
    clastPos = frame["CascadeLast_DC"].pos
    string1Pos = common_variables.hit_statistics.calculate_cog(geometry_,frame["String1Pulses"].apply(frame))
    vertDiff = clastPos-string1Pos 
####    print vertDiff.magnitude,clastPos.z,string1Pos.z,vertDiff.z
    if(vertDiff.magnitude<50):
      return True
    else:
      return False
  else:
    return False

tray.Add(FiltCut)

#tray.AddModule('I3CLastModule', 'clast',
#        InputReadout=   'TWOfflinePulsesDC',#Clean
#        Name=           'CLastTWOff_DC',
#        EnergyParam0=   -3.3,
#        EnergyParam1=   9.2,
#        EnergyParam2=   -9.7,
#        EnergyParam3=   5.3,
#        EnergyParam4=   -1.4,
#        EnergyParam5=   0.134)


tray.AddModule('I3StaticTWC<I3RecoPulseSeries>', 'L2_static-twc',
               InputResponse     =  'OfflinePulses',        # ! Input response
               OutputResponse    =  'OfflinePulses_TW',           # ! Output response
               TriggerConfigIDs  =  [1011],                       # ! Trigger Config ID
               TriggerName       =  'I3TriggerHierarchy',         # Default
               FirstTriggerOnly  =  True,                         # Only take the time window around the first trigger
               WindowMinus       =  4000.0*I3Units.ns ,           # ! Backward time window for SMT3 Trigger
               WindowPlus        =  6000.0*I3Units.ns             # ! Forward time window  for SMT3 Trigger
               )

tray.AddModule('I3SeededRTHitMaskingModule', 'L2_sRTCleaning',
               InputResponse    = 'OfflinePulses_TW',
               OutputResponse   = 'OfflinePulses_sRT',
               RTRadius         = 200,
               RTTime           = 700,
               DeepCoreRTRadius         = 100,
               DeepCoreRTTime           = 400,
               MaxIterations    = 3,
               Seeds            = 'HLCcore',
               HLCCoreThreshold = 2
               )

tray.Add("PulseCore",
         InputPulses="OfflinePulses_sRT",
         OutputName="String3Pulses")

#tray.Add("PulseCore",
#         InputPulses="OfflinePulses_sRT",
#         OutputName="String4Pulses",
#         NStrings=1)

tray.Add("PulseCore",
         InputPulses="OfflinePulses_sRT",
         OutputName="String1Pulses",
         NStrings=1)


def MaskPulses(frame):
  frame['Out1Pulses']= dataclasses.I3RecoPulseSeriesMapMask(frame, 'OfflinePulses_sRT', selector)

#tray.AddModule('NoiseEngine<I3RecoPulse>','L3_NoiseEngine',
#               HitSeriesName = 'SRTTWOfflinePulsesDC',
#               HitSeriesName = 'String3Pulses',
#               OutputName    = 'NoiseEngine_S3bool'
#               )

tray.Add(PCVertCut)

'''
tray.AddModule('NoiseEngine<I3RecoPulse>','L3_NoiseEngine',
               HitSeriesName = 'OfflinePulses',
#               HitSeriesName = 'String3Pulses',
               OutputName    = 'NoiseEngine_S3bool'
               )
'''
#tray.AddSegment(level3_DeepCore.DeepCoreCuts, "L3DeepCoreCuts")

#tray.Add(ZTravelCut)

#tray.Add(MinHitCut)

#tray.Add(VertDiffCut)

#tray.Add(FPosCut)

#tray.Add(MPEZenCut)

#tray.Add(MyCausVetCut)

#tray.Add(NEBool,'nebool')

#tray.AddModule(I3CutL7Module, 'cutL7',
#               maxNVetoHits = 2
#               )

#tray.AddModule(insert_weight,'insert_weight')

#tray.AddModule(insert_corsikaweight,'insert_corsikaweight')

#tray.Add(noiseWeight,"nWeight")

#tray.Add(uwcorsikaWeight,"uwcWeight")

tray.Add("I3Writer",
  Streams           = [icetray.I3Frame.DAQ, icetray.I3Frame.Physics],
  DropOrphanStreams = [icetray.I3Frame.DAQ],
#  filename='/data/ana/LE/Background/Bundles/BundData/'+sys.argv[1])
  filename='/data/user/mamday/icesim/scripts/output/Corsika/'+sys.argv[1])
#  filename='/data/ana/LE/Background/NuMu/'+sys.argv[1])
####  filename='/data/user/mamday/icesim/scripts/output/Noise/'+sys.argv[1])


tray.Execute()

print "Tot Weight: ",sum_weight
