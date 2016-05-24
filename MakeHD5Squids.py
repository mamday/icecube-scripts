#!/usr/bin/env python
#nuSQUIDS specific stuff
import nuSQUIDSpy as nsq
import nuSQUIDSTools

import numpy as np
import tables
import math
from glob import glob
import os
import sys

#this_zen = float(sys.argv[1])
#mtbins = int(sys.argv[2])
#ttbins = int(sys.argv[3])
#etbins = int(sys.argv[2])
#embins = int(sys.argv[3])
mutau = float(sys.argv[1])
tautau = float(sys.argv[2])
th23 = float(sys.argv[3])
dm2 = float(sys.argv[4])
#my_etaus = np.linspace(-0.2,0.2,etbins) 
#my_emus = np.linspace(-0.2,0.2,embins) 
#my_mutaus = np.linspace(-0.015,0.015,mtbins) 
#my_tautaus = np.linspace(-0.1,0.1,ttbins) 

beg_ene = 1 
end_ene = 1011

def SetNSQParams(nuSQ,flavor_id):
  print th23,dm2*.001
  nuSQ.Set_MixingAngle(0,1,0.59);
  nuSQ.Set_MixingAngle(0,2,0.154085);
  nuSQ.Set_MixingAngle(1,2,th23);
  nuSQ.Set_SquareMassDifference(1,7.54e-05);
  nuSQ.Set_SquareMassDifference(2,dm2*.001);
  nuSQ.Set_CPPhase(0,2,0.0);
#  nuSQ.Set_h_max( 100.0*nuSQ.units.km );
  nuSQ.Set_rel_error( 1.0e-15);
  nuSQ.Set_abs_error( 1.0e-15);
  if(flavor_id==1):
    st =np.tile((np.array([1 for i in nuSQ.GetERange()]).reshape((200,1)))*(np.array([0.,1.,0.]).reshape(1,3)),(100,1,1))
    #st =np.tile((np.array([1 for i in nuSQ.GetERange()]).reshape((200,1,1))*np.array([1,1]).reshape((2,1))*np.array([0.,1.,0.]).reshape(1,3)),(100,1,1,1))
  if(flavor_id==0):
    st =np.tile((np.array([1 for i in nuSQ.GetERange()]).reshape((200,1)))*(np.array([1.,0.,0.]).reshape(1,3)),(100,1,1))
#    st =np.tile((np.array([1 for i in nuSQ.GetERange()]).reshape((200,1,1))*np.array([1,1]).reshape((2,1))*np.array([1.,0.,0.]).reshape(1,3)),(100,1,1,1))
#  nuSQ.Set_Body(nsq.EarthAtm())
#  nuSQ.Set_Track(nsq.EarthAtm.Track(np.arccos(zen)))
  print st.shape
  nuSQ.Set_initial_state(st,nsq.Basis.flavor);
  nuSQ.EvolveState() 

#def create_nuSQuIDS(mutauBins,tautauBins):
def create_nuSQuIDS():
  global numuSQUIDSDict, numubarSQUIDSDict, nueSQUIDSDict, nuebarSQUIDSDict
#    print 'MT: ',etau 
#      print 'TT: ',tautau 
  #nuSQBar = nsq.nuSQUIDSAtm(-1,1,400,mutau,tautau,0.0,0.0,beg_ene,end_ene,200,3,nsq.NeutrinoType.antineutrino,True,False)
  nuSQ = nsq.nuSQUIDSAtm(-1,1,100,mutau,tautau,0.0,0.0,beg_ene,end_ene,200,3,nsq.NeutrinoType.neutrino,True,False)
  #print nuSQ.GetNumCos(),nuSQ.GetNumE()
#Muon neutrinos
  SetNSQParams(nuSQ,1)
  #SetNSQParams(this_zen,nuSQBar,1)
  numu_filename = "/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/FourD/Atm-NuMu-Squid-%.4fMT_%.3fTT_%.3fTH_%.3fDM.hdf5" % (mutau,tautau,th23,dm2)
#   numubar_filename = "/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/Atm-NuMuBar-Squid-%.4fET%.3fEM.hdf5" % (mutau,tautau)
  nue_filename = "/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/FourD/Atm-NuE-Squid-%.4fMT_%.3fTT_%.3fTH_%.3fDM.hdf5" % (mutau,tautau,th23,dm2)
#  nuebar_filename = "/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/Atm-NuEBar-Squid-%.4fET%.3fEM.hdf5" % (mutau,tautau)
#  groupname = "/NuMu%.4fET%.3fEM" % (mutau, tautau)
  #nuSQ.WriteStateHDF5(filename,groupname,True,"/")
#Current output
  nuSQ.WriteStateHDF5(numu_filename)
  #nuSQBar.WriteStateHDF5(numubar_filename)
#Electron neutrinos
  SetNSQParams(nuSQ,0)
  #SetNSQParams(this_zen,nuSQBar,0)
#Current output
  nuSQ.WriteStateHDF5(nue_filename)
  #nuSQBar.WriteStateHDF5(nuebar_filename)

#Create nuSQUIDS objects for given sets of mutau and tautau, th23 and dm2 values 
####create_nuSQuIDS(my_mutaus,my_tautaus)
create_nuSQuIDS()

