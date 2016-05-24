#!/usr/bin/env python

import icecube
from icecube import dataclasses, dataio, icetray
from icecube import MuonGun
from icecube.MuonGun import load_model, EnergyDependentSurfaceInjector, ConstantSurfaceScalingFunction, StaticSurfaceInjector, Cylinder, OffsetPowerLaw


import  numpy, math

from I3Tray import *
file_list = sys.argv[2:]
n_files = len(file_list)

dcSurface = Cylinder(500*I3Units.m, 150*I3Units.m, dataclasses.I3Position(29.3,52.6,-300))
icSurface = Cylinder(1600*I3Units.m, 800*I3Units.m)

def SurfEneCut(frame):
  dcPart = MuonGun.muons_at_surface(frame,dcSurface)
  max_ene = 0
#  if(frame.Has('I3MCTree')):
#    if(frame["I3MCTree"].most_energetic_muon):
#      if(frame["I3MCTree"].most_energetic_muon.energy<500):
#        return False
#    else:
#      return False
#  else:
#    return False
  if(len(dcPart)>0):
    for i in xrange(len(dcPart)):
      if(dcPart[i].energy>max_ene):
        max_ene = dcPart[i].energy
    if(max_ene>0):
#      print max_ene, len(dcPart)
      return True
    else:
      return False
  else:
    return False 

def uwcorsikaWeight(frame):
  weight = 1/(4.014*n_files)
  frame["weight"] = dataclasses.I3Double(weight)

tray = I3Tray()

tray.Add("I3Reader",FilenameList = sys.argv[2:])

tray.Add(SurfEneCut, Streams=[icetray.I3Frame.DAQ])

tray.Add(uwcorsikaWeight, Streams=[icetray.I3Frame.DAQ])

tray.Add("I3Writer",
  DropOrphanStreams = [icetray.I3Frame.Physics],
  filename=sys.argv[1])

tray.Execute()

