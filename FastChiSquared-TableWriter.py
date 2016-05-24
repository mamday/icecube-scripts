#!/usr/bin/env python
#Basically everything I do is in the form of terrible table writers...
import icecube

from icecube import icetray, dataclasses, dataio, hdfwriter
from I3Tray import *
from icecube.icetray import I3Units
from icecube.hdfwriter import I3HDFTableService
from icecube.tableio import I3TableWriter
from icecube import neutrinoflux, common_variables
from icecube.common_variables import direct_hits


import numpy as np
import math
from glob import glob
import os
import sys

tray = I3Tray()

numu_flux = neutrinoflux.ConventionalNeutrinoFlux("honda2006_numu")
nue_flux = neutrinoflux.ConventionalNeutrinoFlux("honda2006_nue")

gcdfile = dataio.I3File("/data/user/mamday/icetray/data/GeometryFiles/GeoCalibDetectorStatus_IC86.55697_corrected_V2.i3")
geo_frame = gcdfile.pop_frame()
while not geo_frame.Has('I3Geometry'): geo_frame = gcdfile.pop_frame()
geometry_ = geo_frame.Get('I3Geometry')

infile = sys.argv[1]
#infile = "/data/user/mamday/nuSQuIDS/nuSQuIDS/resources/python/bindings/genie_ic.1460.000000.i3"
#infile = "/data/user/mamday/nuSQuIDS/nuSQuIDS/resources/python/bindings/genie_ic.1260.000000.i3"
#infile = "/data/user/mamday/nuSQuIDS/nuSQuIDS/resources/python/bindings/genie_ic.1660.000000.i3"
#infile = "/data/user/jpyanez/final_sample/neutrino2015_finalLevel/14500/genie_ic.14500.000000.i3.gz"

#tray.AddModule('I3Reader','reader',FilenameList = ["/data/user/mamday/icetray/data/GeometryFiles/GeoCalibDetectorStatus_IC86.55697_corrected_V2.i3",infile], SkipKeys = ["TimeShift"])
#tray.AddModule('I3Reader','reader',FilenameList = ["/data/user/mamday/icetray/data/GeometryFiles/GeoCalibDetectorStatus_pingu_V36_Zezel_40_s22_d3.i3",infile], SkipKeys = ["TimeShift"])
tray.AddModule('I3Reader','reader',FilenameList = ["/data/user/mamday/icetray/data/GeometryFiles/GeoCalibDetectorStatus_IC86.55697_corrected_V2.i3",infile], SkipKeys = ["TimeShift"])

#out_num = int(sys.argv[1])
#g_ind = infile.index('genie')
g_ind = infile.index('Level2')
#g_ind = infile.index('data_')
i3_ind = infile.index('i3')
out_sys = infile[g_ind:i3_ind-1] 


#hdf = I3HDFTableService('/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/Weights/%s.hd5' % out_sys)
#hdf = I3HDFTableService('/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/Weights/JPIC863-Muons.hd5')
hdf = I3HDFTableService('/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/PRDWeights/%s.hd5' % out_sys)
#hdf = I3HDFTableService('/data/user/mamday/nuSQuIDS/nuSQuIDS/resources/python/bindings/HD5PhysFiles/NuMu/PINGU-NuMu-MC-ChiSquared-%04d.hd5' % out_num)
#Juan Pablo's
####numu_nfiles = 4000
#nue_nfiles = 2700
####nutau_nfiles = 1400

#nfiles = int(sys.argv[4])
nfiles = 1 

#PINGU
#numu_nfiles = 192 

def DoPCuts(frame):
  if(frame["Cuts_V5_Step1"].value==1 and frame["Cuts_V5_Step2"].value==1):
    return True
  else:
    return False

#tray.Add(DoPCuts)

def DoJPCuts(frame):
  fin_muon = frame["SANTA_Fit_Muon"]
#  fin_muon = frame["SANTA_Muon"]
  pid_val = frame["SANTA_PID"]
  if(frame.Has("SANTA_rejected_old")):
    r_bool = frame["SANTA_rejected_old"]
    if(r_bool.value==0):
      pass 
    else:
      return False
#  if(frame.Has("SANTA_FitResultsZenith_MS_Muon")):
#    ms_muon = frame["SANTA_FitResultsZenith_MS_Muon"]
  if(frame.Has("SANTA_FitType")):
#    ms_muon = frame["SANTA_FitResultsZenith_MS_Muon"]
    f_type = frame["SANTA_FitType"]
#    if(ms_muon.dir.zenith==fin_muon.dir.zenith):
#      print 'MS',pid_val.value
    if(f_type==2):
      if(pid_val.value<0.8):
        return True
      else:
        return False
#  if(frame.Has("SANTA_FitResultsZenith_SS3D_Muon")):
#    ss_muon = frame["SANTA_FitResultsZenith_SS3D_Muon"]
#    if(ss_muon.dir.zenith==fin_muon.dir.zenith):
####      print 'SS',pid_val.value
    if(f_type==1):
      if(pid_val.value<0.6):
        return True
      else:
        return False

#tray.Add(DoJPCuts)

def insert_weight(frame):
    if "I3MCTree" and "I3MCWeightDict" in frame:
      tree = frame["I3MCTree"]
      weight_dict = frame["I3MCWeightDict"]
      nu_type = tree.most_energetic_primary.type
      nu_energy = tree.most_energetic_primary.energy
      nu_costheta = -1*math.cos(tree.most_energetic_primary.dir.zenith)
      #atmoflux = flux.getFlux(nu_type, nu_energy, nu_costheta)
      if('Bar' in str(nu_type)):
        atmoflux_nue = nue_flux.getFlux(dataclasses.I3Particle.ParticleType.NuEBar, nu_energy, nu_costheta)
        atmoflux_numu = numu_flux.getFlux(dataclasses.I3Particle.ParticleType.NuMuBar, nu_energy, nu_costheta)
      else:
        atmoflux_nue = nue_flux.getFlux(dataclasses.I3Particle.ParticleType.NuE, nu_energy, nu_costheta)
        atmoflux_numu = numu_flux.getFlux(dataclasses.I3Particle.ParticleType.NuMu, nu_energy, nu_costheta)
#Calculate the final oscillated weight
      nue_weight = weight_dict["OneWeight"]*atmoflux_nue/(nfiles*weight_dict["NEvents"])
      numu_weight = weight_dict["OneWeight"]*atmoflux_numu/(nfiles*weight_dict["NEvents"])
      #print nu_type,mt,tt,tab_energy,tab_costheta,weight
      frame["UnOscWeightNuE"] = dataclasses.I3Double(nue_weight)
      frame["UnOscWeightNuMu"] = dataclasses.I3Double(numu_weight)

tray.AddModule(insert_weight,'insert_weight')

def AddDHits(frame):
  dh_defs = direct_hits.default_definitions
  
  if(frame['I3MCTree'].most_energetic_muon): 
    direct_hits_map = direct_hits.calculate_direct_hits(
      dh_defs,
      geometry_,
      frame['MaskedOfflinePulses'].apply(frame),
      frame['I3MCTree'].most_energetic_muon
    )
 
    frame["DirectHits_A"]  = direct_hits_map['A']
    frame["DirectHits_B"]  = direct_hits_map['B']

#tray.Add(AddDHits)

#tray.AddModule(I3TableWriter,'writer', tableservice = [hdf], SubEventStreams = ["in_ice"],keys=["UnOscWeightNuMu","UnOscWeightNuE","trueNeutrino","trueMuon","trueCascade","SANTA_Muon","SANTA_Cascade","I3MCWeightDict"])
#tray.AddModule(I3TableWriter,'writer', tableservice = [hdf], SubEventStreams = ["in_ice"],keys=["UnOscWeightNuMu","UnOscWeightNuE","trueNeutrino","trueMuon","trueCascade","SANTA_Fit_Muon","SANTA_Fit_CascadeHad","I3MCWeightDict"])
#tray.AddModule(I3TableWriter,'writer', tableservice = [hdf], SubEventStreams = ["InIceSplit"],keys=["UnOscWeightNuMu","UnOscWeightNuE","trueNeutrino","trueMuon","trueCascade","SANTA_Fit_Muon","SANTA_Fit_CascadeHad","SANTA_Muon","SANTA_Cascade","I3MCWeightDict"])
tray.AddModule(I3TableWriter,'writer', tableservice = [hdf], SubEventStreams = ["in_ice"],keys=["UnOscWeightNuMu","UnOscWeightNuE","trueNeutrino","trueMuon","trueCascade","SANTA_Fit_Muon","SANTA_Fit_CascadeHad","SANTA_Muon","SANTA_Cascade","I3MCWeightDict","OneWeight"])

#tray.Execute(3600)
tray.Execute()

