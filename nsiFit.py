#!/usr/bin/env python
from __future__ import division
import resource
import fcntl
import nuSQUIDSpy as nsq
import nuSQUIDSTools 

#import icecube
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle
import tables
import pylab
import numpy
import scipy
from scipy import *
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline
from pylab import *
import minuit2
from numpy.polynomial.polynomial import polyfit

import multiprocessing
from multiprocessing import Pool

#from icecube import dataclasses, phys_services, icetray
#from icecube.icetray import I3Units

import os,glob,sys
#Global variables
my_mutaus = numpy.linspace(-0.015,0.015,31)
my_tautaus = numpy.linspace(-0.1,0.1,21)

#def readPickleFiles(in_num=1460,nu_flav=('mu','base')):

def readHD5Files(in_num=1460,nu_flav=('mu','base'),load_splines = True):
  global my_mutaus,my_tautaus
#Get information from all baseline files 
  hd5list = glob.glob("/data/user/mamday/nuSQuIDS/nuSQuIDS/resources/python/bindings/HD5PhysFiles/All/CombWeights-%d*.hd5" % in_num)

  hdf_tabs = {}
  nuMuWeight = []
  nuEWeight = []
  s_MuonEnergy = []
  s_MuonZenith = []
  s_CascadeEnergy = []
  t_NeutrinoEnergy = []
  t_NeutrinoZen = []
  t_NeutType = []
  m_weight_dict = {}
  e_weight_dict = {}
  if(load_splines):
    for mt in my_mutaus:
        for tt in my_tautaus:
            m_weight_dict[(mt,tt)]=[]
            e_weight_dict[(mt,tt)]=[]
#Get weights for each event from the hd5 files
  for it in xrange(len(hd5list)):
    hdf_tabs[it]=tables.File(hd5list[it])
    #print in_num 
    if(nu_flav[0]=='mu'):
      nuMuWeight.extend((1/4000)*hdf_tabs[it].root.UnOscWeightNuMu.cols.value[:])
      nuEWeight.extend((1/4000)*hdf_tabs[it].root.UnOscWeightNuE.cols.value[:])
    if(nu_flav[0]=='e'):
      nuMuWeight.extend((1/2700)*hdf_tabs[it].root.UnOscWeightNuMu.cols.value[:])
      nuEWeight.extend((1/2700)*hdf_tabs[it].root.UnOscWeightNuE.cols.value[:])
    if(nu_flav[0]=='tau'):
      nuMuWeight.extend((1/1400)*hdf_tabs[it].root.UnOscWeightNuMu.cols.value[:])
      nuEWeight.extend((1/1400)*hdf_tabs[it].root.UnOscWeightNuE.cols.value[:])
    s_MuonEnergy.extend(hdf_tabs[it].root.SANTA_Muon.cols.energy[:])
    s_MuonZenith.extend(hdf_tabs[it].root.SANTA_Muon.cols.zenith[:])
    s_CascadeEnergy.extend(hdf_tabs[it].root.SANTA_Cascade.cols.energy[:])
    t_NeutrinoEnergy.extend(hdf_tabs[it].root.trueNeutrino.cols.energy[:])
    t_NeutrinoZen.extend(hdf_tabs[it].root.trueNeutrino.cols.zenith[:])
    t_NeutType.extend(hdf_tabs[it].root.trueNeutrino.cols.type[:])

#Have to format the numbers just so because I accidentally made the output name kind of difficult to parse and haven't fixed it as of 3/18/2015
    if(load_splines):
      w_flav = ''
      if(nu_flav[0]=='mu'): 
        w_flav = 'mu'
      if(nu_flav[0]=='e'): 
        w_flav = 'e'
      if(nu_flav[0]=='tau'): 
        w_flav = 'tau'
      for mutau in my_mutaus:
        for tautau in my_tautaus:
          if(mutau!=0 and tautau!=0):
            e_w_name = "/e%s_weight[%g][%g]" % (w_flav,mutau,tautau)
            m_w_name = "/m%s_weight[%g][%g]" % (w_flav,mutau,tautau)
            e_weight_dict[(mutau,tautau)].extend(hdf_tabs[it].getNode(e_w_name))
            m_weight_dict[(mutau,tautau)].extend(hdf_tabs[it].getNode(m_w_name))
#          if(mutau==-0.01 and tautau==-0.1): print 'Here',len(m_weight_dict[(mutau,tautau)]),hdf_tabs[it].getNode(m_w_name)[:10]
          elif(mutau==0 and tautau!=0):
            e_w_name = "/e%s_weight[0.0][%g]" % (w_flav,tautau)
            m_w_name = "/m%s_weight[0.0][%g]" % (w_flav,tautau)
            e_weight_dict[(mutau,tautau)].extend(hdf_tabs[it].getNode(e_w_name))
            m_weight_dict[(mutau,tautau)].extend(hdf_tabs[it].getNode(m_w_name))
         # if(tautau==-0.1): print 'And Here',len(m_weight_dict[(mutau,tautau)]),hdf_tabs[it].getNode(m_w_name)[:10]
          elif(tautau==0 and mutau!=0):
            e_w_name = "/e%s_weight[%g][0.0]" % (w_flav,mutau)
            m_w_name = "/m%s_weight[%g][0.0]" % (w_flav,mutau)
            e_weight_dict[(mutau,tautau)].extend(hdf_tabs[it].getNode(e_w_name))
            m_weight_dict[(mutau,tautau)].extend(hdf_tabs[it].getNode(m_w_name))
         # if(mutau==-0.01): print 'And and Here',len(m_weight_dict[(mutau,tautau)]),len([i*j for i,j in zip(hdf_tabs[it].root.UnOscWeightNuMu.cols.value[:],hdf_tabs[it].getNode(m_w_name))])
          else:
            e_w_name = "/e%s_weight[0.0][0.0]" % (w_flav)
            m_w_name = "/m%s_weight[0.0][0.0]" % (w_flav)
            e_weight_dict[(mutau,tautau)].extend(hdf_tabs[it].getNode(e_w_name))
            m_weight_dict[(mutau,tautau)].extend(hdf_tabs[it].getNode(m_w_name))
         # print 'The Last',len(m_weight_dict[(mutau,tautau)])
    hdf_tabs[it].close()
    #m_w_name = "/m%s_weight[0.0][0.0]" % (w_flav)
    #print in_num,hd5list[it],hdf_tabs[it].getNode(m_w_name)[:10],hdf_tabs[it].root.trueNeutrino.cols.energy[:10],hdf_tabs[it].root.trueNeutrino.cols.zenith[:10]
  return  nuMuWeight,nuEWeight,s_MuonEnergy,s_MuonZenith,s_CascadeEnergy,t_NeutrinoEnergy,t_NeutrinoZen,t_NeutType,m_weight_dict,e_weight_dict

#Create splines of NSI weights for each event
def makeNSISplines(m_weight_dict,e_weight_dict,mode=0):
  global my_mutaus,my_tautaus
  if(mode==0):
    m_spline2d = [] 
    e_spline2d = [] 
    e_weight_arr=[numpy.zeros((len(my_mutaus),len(my_tautaus))) for i in xrange(len(e_weight_dict[(0,0)]))]
    m_weight_arr=[numpy.zeros((len(my_mutaus),len(my_tautaus))) for i in xrange(len(m_weight_dict[(0,0)]))]

#Change the dictionary of weights for each value of the NSI parameters epsilon_mutau and epsilon_tautau into two dimensional arrays of all the values of the weights for each event
    for mt in xrange(len(my_mutaus)):
      for tt in xrange(len(my_tautaus)):
        for i in xrange(len(e_weight_dict[(0.0,0.0)])): 
          m_weight_arr[i][mt][tt] = m_weight_dict[(my_mutaus[mt],my_tautaus[tt])][i]
          e_weight_arr[i][mt][tt] = e_weight_dict[(my_mutaus[mt],my_tautaus[tt])][i]
#Create splines to be able to access any value of the weights for each event
    for val in xrange(len(e_weight_dict[(0.0,0.0)])):
        m_spline2d.append(scipy.interpolate.RectBivariateSpline(my_mutaus,my_tautaus,m_weight_arr[val]))
        e_spline2d.append(scipy.interpolate.RectBivariateSpline(my_mutaus,my_tautaus,e_weight_arr[val]))
  if(mode==1):
    m_spline2d = {} 
    e_spline2d = {} 
    for mt in xrange(len(my_mutaus)):
      for tt in xrange(len(my_tautaus)):
        m_spline2d[(my_mutaus[mt],my_tautaus[tt])] = m_weight_dict[(my_mutaus[mt],my_tautaus[tt])]
        e_spline2d[(my_mutaus[mt],my_tautaus[tt])] = e_weight_dict[(my_mutaus[mt],my_tautaus[tt])]
  return m_spline2d,e_spline2d

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
    st =(np.array([1 for i in nuSQ.GetERange()]).reshape((2,1)))*(np.array([0.,1.,0.]).reshape(1,3))
  if(flavor_id==0):
    st =(np.array([1 for i in nuSQ.GetERange()]).reshape((2,1)))*(np.array([1.,0.,0.]).reshape(1,3))
  nuSQ.Set_Body(nsq.EarthAtm())
  nuSQ.Set_Track(nsq.EarthAtm.Track(np.arccos(zen)))
  nuSQ.Set_initial_state(st,nsq.Basis.flavor);
  nuSQ.EvolveState()

def makenuSQuIDS(ene,zen,flav,n_type,mutau=0.0,tautau=0.0,mode=0,e_SQuIDS=None,m_SQuIDS=None):
  if(mode==0):
    if(n_type>0):
      nuSQ = nsq.nuSQUIDSNSI(mutau,0.0,tautau,0.0,0.0,math.floor(ene),math.ceil(ene),2,3,nsq.NeutrinoType.neutrino,True,False)
    if(n_type<0):
      nuSQ = nsq.nuSQUIDSNSI(mutau,0.0,tautau,0.0,0.0,math.floor(ene),math.ceil(ene),2,3,nsq.NeutrinoType.antineutrino,True,False)
    if(flav=='e'):
      SetNSQParams(numpy.cos(zen),nuSQ,0)
    if(flav=='mu'):
      SetNSQParams(numpy.cos(zen),nuSQ,1)
    return nuSQ.EvalFlavor(0,ene*nuSQ.units.GeV,0),nuSQ.EvalFlavor(1,ene*nuSQ.units.GeV,0),nuSQ.EvalFlavor(2,ene*nuSQ.units.GeV,0)
  if(mode==1):
    pytpe = None
    if(n_type>0):
      if(flav=='e'):
        ptype = 'NuE' 
      if(flav=='mu'):
        ptype = 'NuMu' 
    if(n_type<0):
      if(flav=='e'):
        ptype = 'NuEBar' 
      if(flav=='mu'):
        ptype = 'NuMuBar' 
    file_name = "/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/ZenWeights/Switch%s%.4fET%.3fEM.hd5" % (ptype,mutau,tautau)
    e_vals = []
    m_vals = []
    t_vals = []
    zen_val = round(numpy.cos(zen),2)
    if(zen_val<-0.995):
      zen_val=-0.995
    group_name = "%s%.4fET%.3fEM%.3f" % (ptype,mutau,tautau,zen_val)
    nuSQ = None
    if(flav=='e'):
      if(not((ptype,mutau,tautau,zen_val) in e_SQuIDS.keys())):
        e_SQuIDS[(ptype,mutau,tautau,zen_val)] = nsq.nuSQUIDS(file_name,group_name)
      nuSQ = e_SQuIDS[(ptype,mutau,tautau,zen_val)]
    if(flav=='mu'):
      if(not((ptype,mutau,tautau,zen_val) in m_SQuIDS.keys())):
        m_SQuIDS[(ptype,mutau,tautau,zen_val)] = nsq.nuSQUIDS(file_name,group_name)
      nuSQ = m_SQuIDS[(ptype,mutau,tautau,zen_val)]
    eWeight = nuSQ.EvalFlavor(0,ene*nuSQ.units.GeV,0)
    mWeight = nuSQ.EvalFlavor(1,ene*nuSQ.units.GeV,0)
    tWeight = nuSQ.EvalFlavor(2,ene*nuSQ.units.GeV,0)
    return eWeight,mWeight,tWeight

class nsiFit(object):

  def __init__(self):
    self.flav_keys = ('e','mu','tau')
    self.sys_keys = ('base','domeffp10','domeffp5','domeffm5','domeffm9','domeffm14','domeffm18','holeice0','holeice30','holeice100') 
    self.nsi_keys = [(p,q) for p in self.flav_keys for q in self.sys_keys] 
    self.e_nsi_splines = dict.fromkeys(self.nsi_keys) 
    self.m_nsi_splines = dict.fromkeys(self.nsi_keys)
    self.e_SQuIDS = {} 
    self.m_SQuIDS = {} 
    self.m_weight = dict.fromkeys(self.nsi_keys)
    self.e_weight = dict.fromkeys(self.nsi_keys)
    self.m_nsi_weight = dict.fromkeys(self.nsi_keys)
    self.e_nsi_weight = dict.fromkeys(self.nsi_keys)
    self.r_mEnergy = dict.fromkeys(self.nsi_keys)
    self.r_mZen = dict.fromkeys(self.nsi_keys)
    self.r_cEnergy = dict.fromkeys(self.nsi_keys)
    self.t_nEnergy = dict.fromkeys(self.nsi_keys)
    self.t_nZen = dict.fromkeys(self.nsi_keys)
    self.t_nType = dict.fromkeys(self.nsi_keys)
    self.eCounts =  dict.fromkeys(self.sys_keys) 
    self.tCounts =  None 
    self.use_splines = True
    self.mode = 0 
    self.file_num_dict = {('e','base'): 1260, ('mu','base'): 1460, ('tau','base'):1660, ('e','domeffp10'):1264,('mu','domeffp10'):1464,('tau','domeffp10'):1664,('e','domeffp5'):1265,('mu','domeffp5'):1465,('tau','domeffp5'):1665,('e','domeffm5'):1261,('mu','domeffm5'):1461,('tau','domeffm5'):1661,('e','domeffm9'):1250,('mu','domeffm9'):1450,('tau','domeffm9'):1650,('e','domeffm14'):1262,('mu','domeffm14'):1462,('tau','domeffm14'):1662,('e','domeffm18'):1263,('mu','domeffm18'):1463,('tau','domeffm18'):1663,('e','holeice0'):1270,('mu','holeice0'):1470,('tau','holeice0'):1670,('e','holeice30'):1271,('mu','holeice30'):1471,('tau','holeice30'):1671,('e','holeice100'):1272,('mu','holeice100'):1472,('tau','holeice100'):1672}
    self.e_bins = numpy.linspace(0,80,8) 
    self.z_bins = numpy.linspace(-1,0,8) 
    self.syst_splines = {'domeff':[[None for i in self.z_bins[:-1]] for j in self.e_bins[:-1]],'holeice':[[None for i in self.z_bins[:-1]] for j in self.e_bins[:-1]]} 

#Calculate weights for certain values of epsilon_mutau(e_mt) and epsilon_tautau(e_tt)
  def CalcNSIWeights(self,e_mt,e_tt,flav):
    e_nsi_weights = numpy.zeros(len(self.t_nEnergy[flav])) 
    m_nsi_weights = numpy.zeros(len(self.t_nEnergy[flav])) 
    if(self.use_splines):
      if(self.mode==0):
        for i in xrange(len(self.e_nsi_splines[flav])):
          e_nsi_weights[i] = float(self.e_nsi_splines[flav][i](e_mt,e_tt))
          m_nsi_weights[i] = float(self.m_nsi_splines[flav][i](e_mt,e_tt))
      if(self.mode==1):
        for i in xrange(len(self.e_nsi_splines[flav][(e_mt,e_tt)])):
          e_nsi_weights[i] = float(self.e_nsi_splines[flav][(e_mt,e_tt)][i])
          m_nsi_weights[i] = float(self.m_nsi_splines[flav][(e_mt,e_tt)][i])
    else:
      for i in xrange(len(self.t_nEnergy[flav])):
       
        eeW,emW,etW = makenuSQuIDS(self.t_nEnergy[flav][i],self.t_nZen[flav][i],'e',self.t_nType[flav][i],e_mt,e_tt,self.mode,self.e_SQuIDS,self.m_SQuIDS)
        meW,mmW,mtW = makenuSQuIDS(self.t_nEnergy[flav][i],self.t_nZen[flav][i],'mu',self.t_nType[flav][i],e_mt,e_tt,self.mode,self.e_SQuIDS,self.m_SQuIDS)
        if(flav[0]=='e'):
          e_nsi_weights[i] = eeW 
          m_nsi_weights[i] = meW 
        if(flav[0]=='mu'):
          e_nsi_weights[i] = emW 
          m_nsi_weights[i] = mmW 
        if(flav[0]=='tau'):
          e_nsi_weights[i] = etW 
          m_nsi_weights[i] = mtW 

    return m_nsi_weights,e_nsi_weights

#Make reference counts with currently defined binning 
  def makeRefCounts(self,e_mt,e_tt,flav,gamma=0,norm_e=1,r_test=False):
    s_totEnergy = [i+j for i,j in zip(self.r_mEnergy[flav],self.r_cEnergy[flav])]
    s_MuonZenith = numpy.cos(self.r_mZen[flav])

#NSI weights. It calculates the NSI weights for each flavor and systematics set once and saves it in self.e_nsi_weights and self.m_nsi_weights 
#This is kind of a horrible way of dealing with wanting to only make weights once and modify the flux systematics... TODO
#    if(self.e_nsi_weight[flav]==None or self.m_nsi_weight[flav]==None):
#      self.m_nsi_weight[flav],self.e_nsi_weight[flav] = self.CalcNSIWeights(e_mt,e_tt,flav)
    #print 'Refs',flav,e_mt,e_tt,self.e_nsi_weight[flav][:10],self.m_nsi_weight[flav][:10]
#Neutrino weights -> Combination of electron neutrino and muon neutrino that oscillate into different flavors, assumes no atmospheric tau neutrinos.
#This is a horrible way to make a test set. TODO
    g_tn_energy = numpy.array([i**gamma for i in self.t_nEnergy[flav]])
    if(r_test):
      tmp_mnsi, tmp_ensi = self.CalcNSIWeights(e_mt,e_tt,flav)
      e_tot_weight = tmp_ensi*g_tn_energy*norm_e*self.e_weight[flav]
      m_tot_weight = tmp_mnsi*g_tn_energy*self.m_weight[flav]
    else:
      if(self.e_nsi_weight[flav]==None or self.m_nsi_weight[flav]==None):
        self.m_nsi_weight[flav],self.e_nsi_weight[flav] = self.CalcNSIWeights(e_mt,e_tt,flav)
      e_tot_weight = self.e_nsi_weight[flav]*g_tn_energy*norm_e*self.e_weight[flav]
      m_tot_weight = self.m_nsi_weight[flav]*g_tn_energy*self.m_weight[flav]
    tot_weight = e_tot_weight+m_tot_weight

#Reference counts
    rCounts, rEdges = numpy.histogramdd((s_totEnergy,s_MuonZenith), bins=(self.e_bins,self.z_bins),weights=tot_weight)
    #print 'RCounts',flav,rCounts[0]
    return 3*31536000*numpy.array(rCounts)

#Create binned total systematic differences
  def makeSysDiffCounts(self,domeff,holeice):
    sysCounts = numpy.zeros([len(self.e_bins)-1,len(self.z_bins)-1]) 

    for ene in xrange(len(self.e_bins)-1):
      for zen in xrange(len(self.z_bins)-1):
        #print 'Sys',domeff,holeice,float(self.syst_splines['domeff'][ene][zen](domeff)),float(self.syst_splines['holeice'][ene][zen](holeice))
        sysCounts[ene][zen] = (float(self.syst_splines['domeff'][ene][zen](domeff))*float(self.syst_splines['holeice'][ene][zen](holeice)))
    #print 'SysCounts:',sysCounts[0]
    return sysCounts

#Calculate LLH for different values of epsilon_mutau and epsilon_tautau, DOM efficiency (domeff), and Hole Ice variations (holeice)
  def llhFunc(self,norm=1.0,e_mt=0.0,e_tt=0.0,domeff=1.0,holeice=50,gamma=0,norm_e=1):
    rCounts = None
    rel_qe = 3.0
    sigma_norm_e  = 0.2
    sigma_rqe  = 0.2
    sigma_gamma   = 0.05
    sigma_domeff  = 0.1 
    sigma_holeice = 0.01 

#Base counts
    for flav in [(p,'base') for p in self.flav_keys]:
      if(rCounts!=None):
        rCounts += norm*self.makeRefCounts(e_mt,e_tt,flav,gamma,norm_e) 
      else:
        rCounts = norm*self.makeRefCounts(e_mt,e_tt,flav,gamma,norm_e)

#Add hole ice and dom efficiency variations
    sCounts = self.makeSysDiffCounts(domeff,holeice)
    rCounts = rCounts*numpy.nan_to_num(sCounts)
#    print 'Comp',domeff,holeice,gamma,norm_e,norm,sum(rCounts[rCounts>=0] - (self.tCounts[rCounts>=0])*log(rCounts[rCounts>=0])),self.tCounts[0],rCounts[0]
#Poisson Likelihood 
    LLH = sum(rCounts[rCounts>=0] - (self.tCounts[rCounts>=0])*log(rCounts[rCounts>=0]))

    LLH += (0.5*((norm_e-1.)/sigma_norm_e)**2 +
            0.5*(gamma/sigma_gamma)**2 +
            0.5*(rel_qe/sigma_rqe)**2 +
            0.5*((domeff-1.0)/sigma_domeff)**2 +
            0.5*(((1/holeice)-0.02)/sigma_holeice)**2 
           )

# Chi-Squared Likelihood
    #LLH2 = sum(((rCounts[rCounts>=0] - self.tCounts[self.tCounts>=0])*(rCounts[rCounts>=0] - self.tCounts[self.tCounts>=0]))/(rCounts[rCounts>=0]))
    #print "LLH:",LLH
    #print "CHi2:",LLH2
    return LLH

#Get splines of systematics differences
  def systDiffs(self):
#TODO: Probably could make this a function also but it is such a pain for no reward of any kind. 
#Make splines for dom efficiency. 'base' has DOM efficiency 1.0, values are 100*(difference from 1.0)
    sel_keys = ('domeffm18','domeffm14','domeffm9','domeffm5','base','domeffp5','domeffp10') 
    diffCounts = dict.fromkeys(sel_keys) 
    wCounts = dict.fromkeys(sel_keys) 
    for syst in sel_keys: 
      diffCounts[syst] = self.eCounts[syst]/self.eCounts['base']
#      print "Counts",self.eCounts[syst],self.eCounts[(syst[0],'base')]
      wCounts[syst] = diffCounts[syst]*(numpy.sqrt(((numpy.sqrt(self.eCounts[syst])/self.eCounts[syst])*(numpy.sqrt(self.eCounts[syst])/self.eCounts[syst])) + ((numpy.sqrt(self.eCounts['base'])/self.eCounts['base'])*(numpy.sqrt(self.eCounts['base'])/self.eCounts['base']))))
    for ene in xrange(len(self.e_bins)-1):
      for zen in xrange(len(self.z_bins)-1):
        syst_diffs = []    
        w_vals = []    
        for syst in sel_keys: 
          syst_diffs.append(diffCounts[syst][ene][zen])     
          w_vals.append(wCounts[syst][ene][zen])
#        print 'DE Diffs',flav,syst,self.e_bins[ene],self.z_bins[zen],diffCounts[(flav,syst)][ene][zen],wCounts[(flav,syst)][ene][zen]
        #k_spline = scipy.interpolate.KroghInterpolator([0.82,0.86,0.91,0.95,1.0,1.05,1.1],syst_diffs)   
        k_spline = np.poly1d(np.polyfit([0.82,0.86,0.91,0.95,1.0,1.05,1.1],syst_diffs,2,rcond=None,w=1/numpy.array(w_vals))) 
        self.syst_splines['domeff'][ene][zen] = k_spline

#        for i in numpy.linspace(0.8,1.1,30):
#          print 'DomEff',i,self.e_bins[ene],self.z_bins[zen],k_spline(i)
#Make splines for hole ice. All hole ice has dom efficiency 0.91, so the 'baseline' set is not actually the 50 cm hole ice baseline 

    sel_keys = ('holeice30','domeffm9','holeice100','holeice0') 
    diffCounts = dict.fromkeys(sel_keys) 
    for syst in sel_keys: 
      diffCounts[syst] = self.eCounts[syst]/self.eCounts['domeffm9']
    for ene in xrange(len(self.e_bins)-1):
      for zen in xrange(len(self.z_bins)-1):
        syst_diffs = []    
        for syst in sel_keys:
          syst_diffs.append(diffCounts[syst][ene][zen])     
        k_spline = scipy.interpolate.BarycentricInterpolator([30,50,100,9E99],syst_diffs)   
        self.syst_splines['holeice'][ene][zen] = k_spline


#Fit the simulation to (mock)D/data 
  def fitFunc(self,e_mt=0.0,e_tt=0.0,use_splines=True,mode=1):
    global my_mutaus,my_tautaus
    self.use_splines = use_splines
    self.mode = mode 
#Get information from files
    for flav in self.nsi_keys: 
#Debugging tool for memory usage. TODO: Probably remove?
#      print 'Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
      in_num = self.file_num_dict[flav] 
#Get information from files
      if(self.use_splines):
        if(self.mode==1):
#Test value
          my_mutaus = [e_mt]
          my_tautaus = [e_tt]
#Systematics value
          if(not(0.0 in my_mutaus)):
            my_mutaus.append(0.0)
          if(not(0.0 in my_tautaus)):
            my_tautaus.append(0.0)
#Fake data value
          if(not(0.0 in my_mutaus)):
            my_mutaus.append(0.0)
          if(not(0.0 in my_tautaus)):
            my_tautaus.append(0.0)
        self.m_weight[flav],self.e_weight[flav],self.r_mEnergy[flav],self.r_mZen[flav],self.r_cEnergy[flav],self.t_nEnergy[flav],self.t_nZen[flav],self.t_nType[flav],m_eps_weights,e_eps_weights = readHD5Files(in_num,flav) 
#Create NSI weight splines
        if(self.mode==0):
          self.m_nsi_splines[flav],self.e_nsi_splines[flav] = makeNSISplines(m_eps_weights,e_eps_weights)
        if(self.mode==1):
          self.m_nsi_splines[flav],self.e_nsi_splines[flav] = makeNSISplines(m_eps_weights,e_eps_weights,mode=1)
      else:
        self.m_weight[flav],self.e_weight[flav],self.r_mEnergy[flav],self.r_mZen[flav],self.r_cEnergy[flav],self.t_nEnergy[flav],self.t_nZen[flav],self.t_nType[flav],m_eps_weights,e_eps_weights = readHD5Files(in_num,flav,False) 

#Make sets and NSI weights for all flavors and systematics (using default physics assumption)
      if(self.eCounts[flav[1]]!=None):
        print flav[1]
        self.eCounts[flav[1]] += self.makeRefCounts(0.0,0.0,flav,0,1,True)
      else:
        print flav[1]
        self.eCounts[flav[1]] = self.makeRefCounts(0.0,0.0,flav,0,1,True)

#Set the "true" Counts
      if(flav[1]=='base'):
        if(self.tCounts!=None):
          self.tCounts += 1.0*self.makeRefCounts(0.0,0.0,flav,0,1,True) 
#          self.tCounts += 1.0*self.makeRefCounts(0.0,0.0,flav,0,1,True) 
        else:
          self.tCounts = 1.0*self.makeRefCounts(0.0,0.0,flav,0,1,True)
#          self.tCounts = 1.0*self.makeRefCounts(0.0,0.0,flav,0,1,True)

#Try to save memory if I am using the splines
#      if(self.use_splines):
#        print 'splines'
#        self.m_nsi_splines[flav] = None
#        self.e_nsi_splines[flav] = None

#Determine systematic uncertainty variations
    self.systDiffs()

#Systematics for test counts
    self.tCounts = numpy.nan_to_num(self.makeSysDiffCounts(1.0,50))*self.tCounts
    print self.tCounts[0]
#Get single test value of LLH
    llh = self.llhFunc(1.0,e_mt,e_tt)
    print 'LLH:',llh
#    llh = self.llhFunc(1,0,0)

    minuit_min = minuit2.Minuit2(self.llhFunc)
    minuit_min.values['norm'] = 1.0
    minuit_min.values['e_mt'] = e_mt 
    minuit_min.values['e_tt'] = e_tt 
    minuit_min.values['domeff'] = 1.00 
    minuit_min.values['holeice'] = 50.0 
    minuit_min.values['gamma'] = 0.0 
    minuit_min.values['norm_e'] = 1.0 

    minuit_min.limits['norm'] = (0.0,1.0) 
    minuit_min.limits['norm_e'] = (0.0,10.0) 
    minuit_min.limits['gamma'] = (-5.0,5.0) 
    minuit_min.limits['e_mt'] = (-0.015,0.015)
    minuit_min.limits['e_tt'] = (-0.1,0.1) 
#    minuit_min.limits['domeff'] = (-30,30) 
    minuit_min.limits['domeff'] = (0.7,1.3) 
    minuit_min.limits['holeice'] = (25,200) 

    minuit_min.errors['norm'] = 0.001 
    minuit_min.errors['e_mt'] = 0.0001 
    minuit_min.errors['e_tt'] = 0.0001 
    minuit_min.errors['domeff'] = 0.005 
    minuit_min.errors['holeice'] = 5.0 
    minuit_min.errors['gamma'] = 0.001 
    minuit_min.errors['norm_e'] = 0.001 

#    minuit_min.fixed['norm'] = True 
#    if(not(self.use_splines)):
    minuit_min.fixed['e_mt'] = True 
    minuit_min.fixed['e_tt'] = True 
#    minuit_min.fixed['domeff'] = True 
#    minuit_min.fixed['holeice'] = True 
#    minuit_min.fixed['gamma'] = True 
#    minuit_min.fixed['norm_e'] = True 

    minuit_min.strategy  = 1
    minuit_min.up        = 0.5
    minuit_min.maxcalls  = 500
    try:
      minuit_min.migrad()
    except:
      try:
        minuit_min.strategy = 2
        minuit_min.printMode = self.printMode
        minuit_min.maxcalls = 1500
        minuit_min.migrad()
      except:
        try:
          minuit_min.simplex()
        except:
          print "All failures"
    fin_vals = '%f,%f,%f,%f,%f,%f,%f,%f,%f,%f \n' % (e_mt,e_tt,minuit_min.fval,minuit_min.values['norm'],minuit_min.values['e_mt'],minuit_min.values['e_tt'],minuit_min.values['domeff'],minuit_min.values['holeice'],minuit_min.values['gamma'],minuit_min.values['norm_e'])
    with open(sys.argv[3],'a') as txt_out:
      #fcntl.flock(txt_out,fcntl.LOCK_EX)
      txt_out.write(fin_vals)
      #fcntl.flock(txt_out, fcntl.LOCK_UN)

#Make some fits
my_fit = nsiFit()
my_fit.fitFunc(float(sys.argv[1]),float(sys.argv[2]),False)
