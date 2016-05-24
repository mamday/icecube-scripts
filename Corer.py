#!/usr/bin/env python

import icecube
from icecube import icetray, dataclasses, phys_services, static_twc, SeededRTCleaning, dataio
from icecube import PulseCore

from I3Tray import *

import os,sys

def FiltCut(frame):
  if(frame.Has("FilterMask")):
    if(frame["FilterMask"]["DeepCoreFilter_11"].condition_passed):
      return True
    else:
      return False
  else:
    return False

tray = I3Tray()

tray.Add("I3Reader", FilenameList=[sys.argv[1],sys.argv[2]])

tray.Add(FiltCut)

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

tray.Add("PulseCore",
         InputPulses="OfflinePulses_sRT",
         OutputName="String1Pulses",
         NStrings=1)

tray.Add("I3Writer",
  DropOrphanStreams = [icetray.I3Frame.DAQ],
  filename=sys.argv[3])

tray.Execute()
