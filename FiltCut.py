#!/usr/bin/env python

import icecube
from icecube import WaveCalibrator, wavedeform, neutrinoflux, TopologicalSplitter, NoiseEngine, dataclasses, clast, dataio, icetray

import numpy, math

from I3Tray import *

sum_weight = 0
n_files = 1

flux = neutrinoflux.ConventionalNeutrinoFlux("honda2006_numu")

def FiltCut(frame):
  if(frame.Has("FilterMask")): 
    if(frame["FilterMask"]["DeepCoreFilter_11"].condition_passed):
      return True
    else:
      return False
  else:
    return False 

def noiseWeight(frame):
  global sum_weight
  weight = (1-(2800*.00003))/(n_files*1000*0.1)
  sum_weight+=weight
  frame["weight"] = dataclasses.I3Double(weight)

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

from icecube import common_variables

tray = I3Tray()

tray.Add("I3Reader",FilenameList = sys.argv[2:])

#tray.AddModule('I3WaveCalibrator', 'domcal')

#tray.AddModule('I3Wavedeform', 'deform')

#tray.AddModule('I3NullSplitter','nullsplitter')

#tray.Add(FiltCut)

tray.Add(insert_weight)

#tray.Add(noiseWeight,"nWeight")

tray.Add("I3Writer",
  DropOrphanStreams = [icetray.I3Frame.DAQ],
  filename=sys.argv[1])

tray.Execute()

print sum_weight
