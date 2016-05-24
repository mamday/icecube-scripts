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


my_mutaus = np.linspace(-0.01,0.01,mtbins) 
my_tautaus = np.linspace(-0.1,0.1,ttbins) 

#print my_mutaus,my_tautaus


squid_file = open('/data/user/mamday/nuSQuIDS/nuSQuIDS/resources/python/bindings/TextFiles/%dMT%dTTZen%.3f-Squid.txt' % (mtbins, ttbins, this_zen),'w')

#numuSQUIDSDict = {}
#numubarSQUIDSDict = {}
#nueSQUIDSDict = {}
#nuebarSQUIDSDict = {}

def SetNSQParams(zen,nuSQ,flavor_id):
  nuSQ.Set("th12",0.59);
  nuSQ.Set("th13",0.154085);
  nuSQ.Set("th23",0.717);
  nuSQ.Set("dm21sq",7.54e-05);
  nuSQ.Set("dm31sq",0.00243);
  nuSQ.Set("delta1",0.0);
  nuSQ.Set("h_max", 100.0*nuSQ.units.km );
  nuSQ.Set("rel_error", 1.0e-15);
  nuSQ.Set("abs_error", 1.0e-15);
  if(flavor_id==1):
    st =(np.array([1 for i in nuSQ.GetERange()]).reshape((200,1)))*(np.array([0.,1.,0.]).reshape(1,3))
  if(flavor_id==0):
    st =(np.array([1 for i in nuSQ.GetERange()]).reshape((200,1)))*(np.array([1.,0.,0.]).reshape(1,3))
  nuSQ.Set_initial_state(st,"flavor");
  nuSQ.Set_Body(nsq.EarthAtm())
  nuSQ.Set_Track(nsq.EarthAtm.Track(np.arccos(zen)))
  nuSQ.EvolveState() 

def create_nuSQuIDS(mutauBins,tautauBins):
  global numuSQUIDSDict, numubarSQUIDSDict, nueSQUIDSDict, nuebarSQUIDSDict
  for mutau in mutauBins:
#    print 'MT: ',mutau 
    for tautau in tautauBins: 
#      print 'TT: ',tautau 
#TODO: Currently taking bin edges, probably want bin centers, oh well
      ind_tup = (mutau,tautau)
      nuSQBar = nsq.nuSQUIDSNSI(10.0,210.0,200,3,"antineutrino",True,False,mutau,tautau)
      nuSQ = nsq.nuSQUIDSNSI(10.0,210.0,200,3,"neutrino",True,False,mutau,tautau)
#Muon neutrinos
      SetNSQParams(this_zen,nuSQ,1)
      SetNSQParams(this_zen,nuSQBar,1)
      for ene in xrange(11,210):
        squid_file.write('NuMu,NuE,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQ.EvalFlavor(0,ene*nuSQ.units.GeV,0))+'\n')
        squid_file.write('NuMuBar,NuEBar,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQBar.EvalFlavor(0,ene*nuSQBar.units.GeV,0))+'\n')
        squid_file.write('NuMu,NuMu,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQ.EvalFlavor(1,ene*nuSQ.units.GeV,0))+'\n')
        squid_file.write('NuMuBar,NuMuBar,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQBar.EvalFlavor(1,ene*nuSQBar.units.GeV,0))+'\n')
        squid_file.write('NuMu,NuTau,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQ.EvalFlavor(2,ene*nuSQ.units.GeV,0))+'\n')
        squid_file.write('NuMuBar,NuTauBar,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQBar.EvalFlavor(2,ene*nuSQBar.units.GeV,0))+'\n')
 
#      numubarSQUIDSDict[ind_tup] = nuSQBar 
#      numuSQUIDSDict[ind_tup] = nuSQ 

#Electron neutrinos
      SetNSQParams(this_zen,nuSQ,0)
      SetNSQParams(this_zen,nuSQBar,0)

      for ene in xrange(11,210):
        squid_file.write('NuE,NuE,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQ.EvalFlavor(0,ene*nuSQ.units.GeV,0))+'\n')
        squid_file.write('NuEBar,NuEBar,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQBar.EvalFlavor(0,ene*nuSQBar.units.GeV,0))+'\n')
        squid_file.write('NuE,NuMu,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQ.EvalFlavor(1,ene*nuSQ.units.GeV,0))+'\n')
        squid_file.write('NuEBar,NuMuBar,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQBar.EvalFlavor(1,ene*nuSQBar.units.GeV,0))+'\n')
        squid_file.write('NuE,NuTau,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQ.EvalFlavor(2,ene*nuSQ.units.GeV,0))+'\n')
        squid_file.write('NuEBar,NuTauBar,'+str(mutau)+','+str(tautau)+','+str(this_zen)+','+str(ene)+','+str(nuSQBar.EvalFlavor(2,ene*nuSQBar.units.GeV,0))+'\n')

#      nuebarSQUIDSDict[ind_tup] = nuSQBar 
#      nueSQUIDSDict[ind_tup] = nuSQ 


#Create nuSQUIDS objects for given sets of mutau and tautau values 
create_nuSQuIDS(my_mutaus,my_tautaus)

squid_file.close()
#print nueSQUIDSDict, nuebarSQUIDSDict, numuSQUIDSDict, numubarSQUIDSDict

