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

this_zen = float(sys.argv[1])
mtbins = int(sys.argv[2])
ttbins = int(sys.argv[3])
#etbins = int(sys.argv[2])
#embins = int(sys.argv[3])

#my_etaus = np.linspace(-0.2,0.2,etbins) 
#my_emus = np.linspace(-0.2,0.2,embins) 
my_mutaus = np.linspace(-0.015,0.015,mtbins) 
my_tautaus = np.linspace(-0.1,0.1,ttbins) 

beg_ene = 1 
end_ene = 1011

def SetNSQParams(zen,nuSQ,flavor_id):
  nuSQ.Set_MixingAngle(0,1,0.59);
  nuSQ.Set_MixingAngle(0,2,0.154085);
  nuSQ.Set_MixingAngle(1,2,0.717);
  nuSQ.Set_SquareMassDifference(1,7.54e-05);
  nuSQ.Set_SquareMassDifference(2,0.00243);
  nuSQ.Set_CPPhase(0,2,0.0);
  nuSQ.Set_h_max( 100.0*nuSQ.units.km );
  nuSQ.Set_rel_error( 1.0e-15);
  nuSQ.Set_abs_error( 1.0e-15);
  if(flavor_id==1):
    st =(np.array([1 for i in nuSQ.GetERange()]).reshape((200,1)))*(np.array([0.,1.,0.]).reshape(1,3))
  if(flavor_id==0):
    st =(np.array([1 for i in nuSQ.GetERange()]).reshape((200,1)))*(np.array([1.,0.,0.]).reshape(1,3))
  nuSQ.Set_Body(nsq.EarthAtm())
  nuSQ.Set_Track(nsq.EarthAtm.Track(np.arccos(zen)))
  nuSQ.Set_initial_state(st,nsq.Basis.flavor);
  nuSQ.EvolveState() 

def create_nuSQuIDS(mutauBins,tautauBins):
  global numuSQUIDSDict, numubarSQUIDSDict, nueSQUIDSDict, nuebarSQUIDSDict
  for mutau in mutauBins:
#    print 'MT: ',etau 
    for tautau in tautauBins: 
#      print 'TT: ',tautau 
#TODO: Currently taking bin edges, probably want bin centers, oh well
      nuSQBar = nsq.nuSQUIDS(beg_ene,end_ene,200,3,nsq.NeutrinoType.antineutrino,True,False)
      nuSQ = nsq.nuSQUIDS(beg_ene,end_ene,200,3,nsq.NeutrinoType.neutrino,True,False)
#Muon neutrinos
      SetNSQParams(this_zen,nuSQ,1)
      SetNSQParams(this_zen,nuSQBar,1)
#      filename = "/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/Squid-Zen%.3f.hdf5" % (this_zen)
      filename = "/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/NewTest.hdf5"
      groupname = "/NuMu%.4fET%.3fEM" % (mutau, tautau)
      print filename,groupname
      nuSQ.WriteStateHDF5(filename,groupname,False,"/")
      #nuSQ.WriteStateHDF5(filename)
      groupname = "/NuMuBar%.4fET%.3fEM" % (mutau, tautau)
#      print groupname
      nuSQBar.WriteStateHDF5(filename,groupname,False,"/")
#Electron neutrinos
      SetNSQParams(this_zen,nuSQ,0)
      SetNSQParams(this_zen,nuSQBar,0)

      groupname = "/NuE%.4fET%.3fEM" % (mutau, tautau)
      nuSQ.WriteStateHDF5(filename,groupname,False,"/")
      groupname = "/NuEBar%.4fET%.3fEM" % (mutau, tautau)
      nuSQBar.WriteStateHDF5(filename,groupname,False,"/")

#Create nuSQUIDS objects for given sets of mutau and tautau values 
create_nuSQuIDS(my_mutaus,my_tautaus)

