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
    #st =np.tile((np.array([1 for i in nuSQ.GetERange()]).reshape((200,1)))*(np.array([0.,1.,0.]).reshape(1,3)),(100,1,1))
    st =np.tile((np.array([1 for i in nuSQ.GetERange()]).reshape((200,1,1))*np.array([1,1]).reshape((2,1))*np.array([0.,1.,0.]).reshape(1,3)),(100,1,1,1))
  if(flavor_id==0):
    #st =np.tile((np.array([1 for i in nuSQ.GetERange()]).reshape((200,1)))*(np.array([1.,0.,0.]).reshape(1,3)),(100,1,1))
    st =np.tile((np.array([1 for i in nuSQ.GetERange()]).reshape((200,1,1))*np.array([1,1]).reshape((2,1))*np.array([1.,0.,0.]).reshape(1,3)),(100,1,1,1))
#  nuSQ.Set_Body(nsq.EarthAtm())
#  nuSQ.Set_Track(nsq.EarthAtm.Track(np.arccos(zen)))
  print st.shape
  nuSQ.Set_initial_state(st,nsq.Basis.flavor);
  nuSQ.EvolveState() 

#def create_nuSQuIDS(mutauBins,tautauBins):
def create_nuSQuIDS():

  nuSQ = nsq.nuSQUIDSAtm(-1,1,100,mutau,tautau,0.0,0.0,beg_ene,end_ene,200,3,nsq.NeutrinoType.both,True,True)
####  nuSQBar = nsq.nuSQUIDSAtm(-1,1,100,mutau,tautau,0.0,0.0,beg_ene,end_ene,200,3,nsq.NeutrinoType.antineutrino,True,True)

#Muon neutrinos
  SetNSQParams(nuSQ,1)
  #SetNSQParams(nuSQBar,1)
  for ene in np.linspace(1,1011,1012):
    print 'Neutrino',ene,nuSQ.EvalFlavor(1,-1.0,ene*nuSQ.units.GeV,0)
  #  print 'Anti-Neutrino',ene,nuSQBar.EvalFlavor(1,-1.0,ene*nuSQBar.units.GeV,0)

  nuSQ.WriteStateHDF5("Test.hd5")

####create_nuSQuIDS(my_mutaus,my_tautaus)
create_nuSQuIDS()

