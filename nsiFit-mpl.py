#!/usr/bin/env python

from __future__ import division
import icecube
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import tables
import pylab
import numpy
import scipy
from scipy import *
from scipy import interpolate
from pylab import *
import minuit2

import multiprocessing
from multiprocessing import Pool

from icecube import dataclasses, phys_services, icetray
from icecube.icetray import I3Units

import os,glob,sys
#Global variables
my_mutaus = numpy.linspace(-0.01,0.01,21)
my_tautaus = numpy.linspace(-0.1,0.1,21)

def readHD5Files(in_num=1460,nu_flav=('mu','base')):
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
  m_weight_dict = {}
  e_weight_dict = {}

  for mt in my_mutaus:
      for tt in my_tautaus:
          m_weight_dict[(mt,tt)]=[]
          e_weight_dict[(mt,tt)]=[]
#Get weights for each event from the hd5 files
  for it in xrange(len(hd5list)):
    hdf_tabs[it]=tables.File(hd5list[it])
    print in_num 
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
#Have to format the numbers just so because I accidentally made the output name kind of difficult to parse and haven't fixed it as of 3/18/2015
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
  return  nuMuWeight,nuEWeight,s_MuonEnergy,s_MuonZenith,s_CascadeEnergy,t_NeutrinoEnergy,m_weight_dict,e_weight_dict

#Create splines of NSI weights for each event
def makeNSISplines(m_weight_dict,e_weight_dict):
  global my_mutaus,my_tautaus
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
  return m_spline2d,e_spline2d



class nsiFit(object):

  def __init__(self):
    self.flav_keys = ('e','mu','tau')
    self.sys_keys = ('base','domeffp10','domeffp5','domeffm5','domeffm9','domeffm14','domeffm18','holeice0','holeice30','holeice100') 
    self.nsi_keys = [(p,q) for p in self.flav_keys for q in self.sys_keys] 
    self.e_nsi_splines = dict.fromkeys(self.nsi_keys) 
    self.m_nsi_splines = dict.fromkeys(self.nsi_keys)
    self.m_weight = dict.fromkeys(self.nsi_keys)
    self.e_weight = dict.fromkeys(self.nsi_keys)
    self.r_mEnergy = dict.fromkeys(self.nsi_keys)
    self.r_mZen = dict.fromkeys(self.nsi_keys)
    self.r_cEnergy = dict.fromkeys(self.nsi_keys)
    self.t_nEnergy = dict.fromkeys(self.nsi_keys)
    self.eCounts =  dict.fromkeys(self.sys_keys) 
    self.file_num_dict = {('e','base'): 1260, ('mu','base'): 1460, ('tau','base'):1660, ('e','domeffp10'):1264,('mu','domeffp10'):1464,('tau','domeffp10'):1664,('e','domeffp5'):1265,('mu','domeffp5'):1465,('tau','domeffp5'):1665,('e','domeffm5'):1261,('mu','domeffm5'):1461,('tau','domeffm5'):1661,('e','domeffm9'):1250,('mu','domeffm9'):1450,('tau','domeffm9'):1650,('e','domeffm14'):1262,('mu','domeffm14'):1462,('tau','domeffm14'):1662,('e','domeffm18'):1263,('mu','domeffm18'):1463,('tau','domeffm18'):1663,('e','holeice0'):1270,('mu','holeice0'):1470,('tau','holeice0'):1670,('e','holeice30'):1271,('mu','holeice30'):1471,('tau','holeice30'):1671,('e','holeice100'):1272,('mu','holeice100'):1472,('tau','holeice100'):1672}
    self.e_bins = numpy.linspace(0,80,8) 
    self.z_bins = numpy.linspace(-1,0,8) 
    self.syst_splines = {'domeff':[[None for i in self.z_bins[:-1]] for j in self.e_bins[:-1]],'holeice':[[None for i in self.z_bins[:-1]] for j in self.e_bins[:-1]]} 

#Calculate weights for certain values of epsilon_mutau(e_mt) and epsilon_tautau(e_tt)
  def CalcNSIWeights(self,e_mt,e_tt,flav):
    e_nsi_weights = numpy.zeros(len(self.e_nsi_splines[flav])) 
    m_nsi_weights = numpy.zeros(len(self.e_nsi_splines[flav])) 

    for i in xrange(len(self.e_nsi_splines[flav])):
      e_nsi_weights[i] = float(self.e_nsi_splines[flav][i](e_mt,e_tt))
      m_nsi_weights[i] = float(self.m_nsi_splines[flav][i](e_mt,e_tt))

    return m_nsi_weights,e_nsi_weights

#Make reference counts with currently defined binning 
  def makeRefCounts(self,e_mt,e_tt,flav,gamma=0,norm_e=1):
    s_totEnergy = [i+j for i,j in zip(self.r_mEnergy[flav],self.r_cEnergy[flav])]
    s_MuonZenith = numpy.cos(self.r_mZen[flav])

#NSI weights
    m_nsi_weights,e_nsi_weights = self.CalcNSIWeights(e_mt,e_tt,flav)

#Neutrino weights -> Combination of electron neutrino and muon neutrino that oscillate into different flavors, assumes no atmospheric tau neutrinos
    g_tn_energy = numpy.array([i**gamma for i in self.t_nEnergy[flav]])
    e_tot_weight = e_nsi_weights*g_tn_energy*norm_e*self.e_weight[flav]
    m_tot_weight = m_nsi_weights*g_tn_energy*self.m_weight[flav]
    tot_weight = e_tot_weight+m_tot_weight

#Reference counts
    rCounts, rEdges = numpy.histogramdd((s_totEnergy,s_MuonZenith), bins=(self.e_bins,self.z_bins),weights=tot_weight)
    return 3*31536000*numpy.array(rCounts)

#Create binned total systematic differences
  def makeSysDiffCounts(self,domeff,holeice):
    sysCounts = numpy.zeros([len(self.e_bins)-1,len(self.z_bins)-1]) 

    for ene in xrange(len(self.e_bins)-1):
      for zen in xrange(len(self.z_bins)-1):
        #print 'Sys',domeff,holeice,float(self.syst_splines['domeff'][ene][zen](domeff)),float(self.syst_splines['holeice'][ene][zen](holeice))
        sysCounts[ene][zen] = (float(self.syst_splines['domeff'][ene][zen](domeff))*float(self.syst_splines['holeice'][ene][zen](holeice)))
    return sysCounts

#Calculate LLH for different values of epsilon_mutau and epsilon_tautau, DOM efficiency (domeff), and Hole Ice variations (holeice)
  def llhFunc(self,norm=1.0,e_mt=0.0,e_tt=0.0,domeff=0,holeice=50,gamma=0,norm_e=1):
    rCounts = None
    rel_qe = 3.0
    sigma_norm_e  = 0.2
    sigma_rqe  = 0.2
    sigma_gamma   = 0.05
    sigma_domeff  = 0.1 
    sigma_holeice = 0.01 

#Base counts
    for flav in [(p,'domeffm9') for p in self.flav_keys]:
      if(rCounts!=None):
        rCounts += norm*self.makeRefCounts(e_mt,e_tt,flav,gamma,norm_e) 
      else:
        rCounts = norm*self.makeRefCounts(e_mt,e_tt,flav,gamma,norm_e)

#Add hole ice and dom efficiency variations
    sCounts = self.makeSysDiffCounts(domeff,holeice)
    rCounts = rCounts*numpy.nan_to_num(sCounts)

#Reference Counts
    tCounts = None
    for flav in [(p,'domeffm9') for p in self.flav_keys]:
      if(tCounts!=None):
        tCounts += 1.0*self.makeRefCounts(0.006,0.1,flav) 
      else:
        tCounts = 1.0*self.makeRefCounts(0.006,0.1,flav)

    tCounts = numpy.nan_to_num(self.makeSysDiffCounts(-9,100))*tCounts 

#Poisson Likelihood 
    LLH = sum(rCounts[rCounts>=0] - (tCounts[tCounts>=0])*log(rCounts[rCounts>=0]))

    LLH += (0.5*((norm_e-1.)/sigma_norm_e)**2 +
            0.5*(gamma/sigma_gamma)**2 +
            0.5*(rel_qe/sigma_rqe)**2 +
            0.5*(((1+(domeff/100))-0.91)/sigma_domeff)**2 +
            0.5*(((1/holeice)-0.02)/sigma_holeice)**2 
           )

# Chi-Squared Likelihood
#    LLH = 31536000*sum(((rCounts[rCounts!=0] - numpy.array(self.eCounts)[numpy.array(self.eCounts)!=0])*(rCounts[rCounts!=0] - numpy.array(self.eCounts)[numpy.array(self.eCounts)!=0]))/(rCounts[rCounts!=0]))
    return LLH

#Get splines of systematics differences
  def systDiffs(self):
#TODO: Probably could make this a function also but it is such a pain for no reward of any kind. 
#Make splines for dom efficiency. 'base' has DOM efficiency 1.0, values are 100*(difference from 1.0)
    sel_keys = ('domeffp10','domeffp5','base','domeffm5','domeffm9','domeffm14','domeffm18') 
    diffCounts = dict.fromkeys(sel_keys) 
    for syst in sel_keys: 
      diffCounts[syst] = self.eCounts[syst]/self.eCounts['domeffm9']
    for ene in xrange(len(self.e_bins)-1):
      for zen in xrange(len(self.z_bins)-1):
        syst_diffs = []    
        for syst in sel_keys:
          syst_diffs.append(diffCounts[syst][ene][zen])     
        k_spline = scipy.interpolate.BarycentricInterpolator([10,5,0,-5,-9,-14,-18],syst_diffs)   
        self.syst_splines['domeff'][ene][zen] = k_spline

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
  def fitFunc(self):
#Get information from files
    for flav in self.nsi_keys: 
      in_num = self.file_num_dict[flav] 
#Get information from files
      self.m_weight[flav],self.e_weight[flav],self.r_mEnergy[flav],self.r_mZen[flav],self.r_cEnergy[flav],self.t_nEnergy[flav],m_eps_weights,e_eps_weights = readHD5Files(in_num,flav) 
#Create NSI weight splines
      self.m_nsi_splines[flav],self.e_nsi_splines[flav] = makeNSISplines(m_eps_weights,e_eps_weights)

#Make "data" from random value of NSI MC
      if(self.eCounts[flav[1]]!=None):
        print flav[1]
        self.eCounts[flav[1]] += self.makeRefCounts(0.0,0.0,flav)
      else:
        print flav[1]
        self.eCounts[flav[1]] = self.makeRefCounts(0.0,0.0,flav)
#Determine systematic uncertainty variations
    self.systDiffs()
#Get single test value of LLH
    llh = self.llhFunc(1,0.006,-0.1)
    print 'LLH:',llh
    llh = self.llhFunc()
    print 'LLH:',llh
#    llh = self.llhFunc(1,0,0)

    minuit_min = minuit2.Minuit2(self.llhFunc)
    minuit_min.values['norm'] = 1.0
    minuit_min.values['e_mt'] = 0.0
    minuit_min.values['e_tt'] = 0.0
    minuit_min.values['domeff'] = -9 
    minuit_min.values['holeice'] = 50.0 
    minuit_min.values['gamma'] = 0.0 
    minuit_min.values['norm_e'] = 1.0 

    minuit_min.limits['norm'] = (0.5,1.5) 
    minuit_min.limits['norm_e'] = (0.0,10.0) 
    minuit_min.limits['gamma'] = (-5.0,5.0) 
    minuit_min.limits['e_mt'] = (-0.01,0.01)
    minuit_min.limits['e_tt'] = (-0.1,0.1) 
    minuit_min.limits['domeff'] = (-30,30) 
    minuit_min.limits['holeice'] = (25,200) 

    minuit_min.errors['norm'] = 0.001 
    minuit_min.errors['e_mt'] = 0.0001 
    minuit_min.errors['e_tt'] = 0.0001 
    minuit_min.errors['domeff'] = 0.5 
    minuit_min.errors['holeice'] = 5.0 
    minuit_min.errors['gamma'] = 0.001 
    minuit_min.errors['norm_e'] = 0.001 

#    minuit_min.fixed['norm'] = True 
#    minuit_min.fixed['e_mt'] = True 
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
    print 'Migrad:',minuit_min.fval,minuit_min.values['norm'],minuit_min.values['e_mt'],minuit_min.values['e_tt'],minuit_min.values['domeff'],minuit_min.values['holeice'],minuit_min.values['gamma'],minuit_min.values['norm_e']
#Fill llh arrays
    eps_arr = numpy.empty([len(my_tautaus),len(my_mutaus)])
    epst_arr = numpy.empty([len(my_tautaus),len(my_mutaus)])
    epsf_arr = numpy.empty([len(my_tautaus),len(my_mutaus)])
    countm = -1
    countt = -1 
    for mt in my_mutaus:
      countt+=1
      countm=-1
      for tt in my_tautaus:
        countm+=1
#        eps_arr[countm][countt] = self.llhFunc(1,minuit_min.values['norm'],mt,tt,minuit_min.values['domeff'],minuit_min.values['holeice'],minuit_min.values['gamma'],minuit_min.values['norm_e'])-minuit_min.fval 
        epst_arr[countm][countt] = self.llhFunc(minuit_min.values['norm'],mt,tt,minuit_min.values['domeff'],minuit_min.values['holeice'],minuit_min.values['gamma'],minuit_min.values['norm_e'])-minuit_min.fval 
#        epsf_arr[countm][countt] = self.llhFunc(4,minuit_min.values['norm'],mt,tt,minuit_min.values['domeff'],minuit_min.values['holeice'],minuit_min.values['gamma'],minuit_min.values['norm_e'])-minuit_min.fval 

#Plot?
    from matplotlib import rcParams
    X, Y = numpy.meshgrid(my_mutaus, my_tautaus)
#    CS = plt.contour(X,Y,eps_arr, [4.6],colors=['r'])
#    CS1 = plt.contour(X,Y,epsf_arr, [4.6],colors=['b'])
    CS2 = plt.contour(X,Y,epst_arr, [4.6],colors=['g'])
    #pylab.ylim(-.05,.05)
    pylab.rc('font', family='serif', size=14)
    pylab.xlabel(r'$\epsilon_{\mu \tau}$', size=30)
    pylab.ylabel('$\\epsilon^{\\prime}$', size=30)
    #plt.clabel(CS, inline=1, fontsize=10)
    label = ['1 Year']
    label1 = ['4 Year']
    label2 = ['3 Year']
    for i in range(len(label)):
#        CS.collections[i].set_label(label[i])
#        CS1.collections[i].set_label(label1[i])
        CS2.collections[i].set_label(label2[i])
    
    pylab.legend(ncol=2)
    pylab.tight_layout()
    pylab.savefig("PrelimNSISys-Reco.pdf")

#Make some fits
my_fit = nsiFit()
my_fit.fitFunc()
#print nsi_splines[1](0,0),m_weight[1],t_mZen[1]
