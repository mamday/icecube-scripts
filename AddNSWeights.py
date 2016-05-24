#!/usr/bin/env python
#nuSQUIDS specific stuff
import nuSQUIDSpy as nsq
import nuSQUIDSTools

import numpy as np
import scipy
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline 
import tables
import math
import os
import sys
import glob
import shutil

mtbins = int(sys.argv[1])
ttbins = int(sys.argv[2])
zbins = int(sys.argv[3])

my_mutaus = np.linspace(-0.015,0.015,mtbins)
my_tautaus = np.linspace(-0.1,0.1,ttbins)
#my_zens = [-0.99,-0.97, -0.95, -0.93, -0.91, -0.89, -0.87, -0.85, -0.83, -0.81, -0.79, -0.77, -0.75, -0.73, -0.71, -0.69, -0.67, -0.65, -0.63, -0.61, -0.59, -0.57, -0.55, -0.53, -0.51, -0.49, -0.47, -0.45, -0.43, -0.41, -0.39, -0.37, -0.35, -0.33, -0.31, -0.29, -0.27, -0.25, -0.23, -0.21, -0.19, -0.17, -0.15, -0.13, -0.11, -0.09, -0.07, -0.05, -0.03, -0.01, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19, 0.21, 0.23, 0.25, 0.27, 0.29, 0.31, 0.33, 0.35, 0.37, 0.39, 0.41, 0.43, 0.45, 0.47, 0.49, 0.51, 0.53, 0.55, 0.57, 0.59, 0.61, 0.63, 0.65, 0.67, 0.69, 0.71, 0.73, 0.75, 0.77, 0.79, 0.81, 0.83, 0.85, 0.87, 0.89, 0.91, 0.93, 0.95, 0.97,0.99]
my_zens = [-1+i*0.0200000000 for i in xrange(zbins) if(i>0 and i<100 and i!=50)] 
#my_zens = [-1+i*0.04 for i in xrange(zbins) if(i>0 and i<50 and i!=25)] 
#print my_zens

#hd5list = glob.glob("/data/user/mamday/nuSQuIDS/nuSQuIDS/resources/python/bindings/HD5PhysFiles/NuMu/AllPINGU.hd5")
#myfile = "Test.hd5"
#outfile = "/data/user/mamday/nuSQuIDS/nuSQuIDS/resources/python/bindings/HD5PhysFiles/NuMu/%s" % myfile

w_file = sys.argv[4]
hd5list = glob.glob(w_file)
a_ind = w_file.index('s/Weights-')
#print hd5list,w_file[a_ind+3:]
myfile = 'NSI-'+w_file[a_ind+2:] 
print myfile
outfile = "/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/Weights/%s" % myfile

heSQUIDDict = {}
hmSQUIDDict = {}
hebSQUIDDict = {}
hmbSQUIDDict = {}

def make_squids(mutauBins,tautauBins,zenBins):
  #print mutauBins,tautauBins,zenBins
  for this_zen in zenBins:
    for mutau in mutauBins:
      for tautau in tautauBins:
        ind_tup = (mutau,tautau,this_zen)
        file_name = "/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/Squid-Zen%.3f.hdf5" % (this_zen)
        groupname = "NuMu%.4fET%.3fEM" % (mutau, tautau)
        #print file_name,groupname
        nuSQ = nsq.nuSQUIDS(file_name,groupname)
        hmSQUIDDict[ind_tup] = nuSQ
        groupname = "NuE%.4fET%.3fEM" % (mutau, tautau)
        #print groupname
        nuSQ = nsq.nuSQUIDS(file_name,groupname)
        heSQUIDDict[ind_tup] = nuSQ
        groupname = "NuMuBar%.4fET%.3fEM" % (mutau, tautau)
        #print groupname
        nuSQBar = nsq.nuSQUIDS(file_name,groupname)
        hmbSQUIDDict[ind_tup] = nuSQBar
        groupname = "NuEBar%.4fET%.3fEM" % (mutau, tautau)
        #print groupname
        nuSQBar = nsq.nuSQUIDS(file_name,groupname)
        hebSQUIDDict[ind_tup] = nuSQBar

make_squids(my_mutaus,my_tautaus,my_zens)

def create_spline(type,ene,mutauBins,tautauBins,zenBins):
  global hebSQUIDDict, hmbSQUIDDict, hmSQUIDDict, heSQUIDDict
  mmSQUIDSDict = {}
  mtSQUIDSDict = {}
  meSQUIDSDict = {}
  emSQUIDSDict = {}
  etSQUIDSDict = {}
  eeSQUIDSDict = {}
  for mutau in mutauBins:
    for tautau in tautauBins:
      nmmz_weights = []
      nmez_weights = []
      nmtz_weights = []
      nemz_weights = []
      neez_weights = []
      netz_weights = []
      for this_zen in zenBins:
#TODO: Argh, argh, argh
#        if(mutau==0.012 and tautau==0.030 and this_zen==-0.66):
#          continue
        ind_tup = (mutau,tautau,this_zen)
        if(type>0):
#          print 'NuMu:',mutau,tautau,this_zen
          nuSQ = hmSQUIDDict[ind_tup]
          nmmz_weights.append(nuSQ.EvalFlavor(1,ene*nuSQ.units.GeV,0))
          nmez_weights.append(nuSQ.EvalFlavor(0,ene*nuSQ.units.GeV,0))
          nmtz_weights.append(nuSQ.EvalFlavor(2,ene*nuSQ.units.GeV,0))
#          print nuSQ.EvalFlavor(1,ene*nuSQ.units.GeV,0)
          nuSQ = heSQUIDDict[ind_tup]
          nemz_weights.append(nuSQ.EvalFlavor(1,ene*nuSQ.units.GeV,0))
          neez_weights.append(nuSQ.EvalFlavor(0,ene*nuSQ.units.GeV,0))
          netz_weights.append(nuSQ.EvalFlavor(2,ene*nuSQ.units.GeV,0))
#          print 'NuE:',mutau,tautau,this_zen
        if(type<0):
#          print 'NuMuBar:',mutau,tautau,this_zen
          nuSQBar = hmbSQUIDDict[ind_tup]
          nmmz_weights.append(nuSQBar.EvalFlavor(1,ene*nuSQBar.units.GeV,0))
#          print nuSQBar.EvalFlavor(1,ene*nuSQBar.units.GeV,0)
          nmez_weights.append(nuSQBar.EvalFlavor(0,ene*nuSQBar.units.GeV,0))
          nmtz_weights.append(nuSQBar.EvalFlavor(2,ene*nuSQBar.units.GeV,0))
          nuSQBar = hebSQUIDDict[ind_tup]
          nemz_weights.append(nuSQBar.EvalFlavor(1,ene*nuSQBar.units.GeV,0))
          neez_weights.append(nuSQBar.EvalFlavor(0,ene*nuSQBar.units.GeV,0))
          netz_weights.append(nuSQBar.EvalFlavor(2,ene*nuSQBar.units.GeV,0))
#          print 'NuEBar:',mutau,tautau,this_zen
#      if(mutau==0.012 and tautau==0.030):
#        zenBins = [-0.98, -0.96, -0.94, -0.92, -0.90, -0.88, -0.86, -0.84, -0.82, -0.8, -0.78, -0.76, -0.74, -0.72, -0.7, -0.68, -0.64, -0.62, -0.6, -0.58, -0.56, -0.54, -0.52, -0.5, -0.48, -0.46, -0.44, -0.42, -0.4, -0.38, -0.36, -0.34, -0.32, -0.30, -0.28, -0.26, -0.24, -0.22, -0.20, -0.18, -0.16, -0.14, -0.12, -0.10, -0.08, -0.06, -0.04, -0.02, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42, 0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58, 0.60, 0.62, 0.64, 0.66, 0.68, 0.7, 0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98]
      me_spline = scipy.interpolate.InterpolatedUnivariateSpline(zenBins,nmez_weights,k=1)
      mm_spline = scipy.interpolate.InterpolatedUnivariateSpline(zenBins,nmmz_weights,k=1)
      mt_spline = scipy.interpolate.InterpolatedUnivariateSpline(zenBins,nmtz_weights,k=1)
      ee_spline = scipy.interpolate.InterpolatedUnivariateSpline(zenBins,neez_weights,k=1)
      em_spline = scipy.interpolate.InterpolatedUnivariateSpline(zenBins,nemz_weights,k=1)
      et_spline = scipy.interpolate.InterpolatedUnivariateSpline(zenBins,netz_weights,k=1)
      mmSQUIDSDict[ind_tup] = mm_spline
      meSQUIDSDict[ind_tup] = me_spline
      mtSQUIDSDict[ind_tup] = mt_spline
      emSQUIDSDict[ind_tup] = em_spline
      eeSQUIDSDict[ind_tup] = ee_spline
      etSQUIDSDict[ind_tup] = et_spline
#      if(mutau==0.012 and tautau==0.030):
#        zenBins = [-0.98, -0.96, -0.94, -0.92, -0.90, -0.88, -0.86, -0.84, -0.82, -0.8, -0.78, -0.76, -0.74, -0.72, -0.7, -0.68, -0.66, -0.64, -0.62, -0.6, -0.58, -0.56, -0.54, -0.52, -0.5, -0.48, -0.46, -0.44, -0.42, -0.4, -0.38, -0.36, -0.34, -0.32, -0.30, -0.28, -0.26, -0.24, -0.22, -0.20, -0.18, -0.16, -0.14, -0.12, -0.10, -0.08, -0.06, -0.04, -0.02, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42, 0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58, 0.60, 0.62, 0.64, 0.66, 0.68, 0.7, 0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98]
  return meSQUIDSDict,mmSQUIDSDict,mtSQUIDSDict,eeSQUIDSDict,emSQUIDSDict,etSQUIDSDict  

def addWeights(mutauBins,tautauBins):
  hdf_tabs = {}
  tab_vals = {}
  tab_desc = {}
  count=0 
  counter=0 
  t_NeutEnergy = []
  t_NeutZenith = []
  t_NeutType = []
  #print myfile,outfile
  out_tabs = tables.File(myfile,"w")
  out_tabs.close()
  shutil.move(myfile,outfile)
  fin_out = tables.File(outfile,"a")
  mefin_weights = {}
  mmufin_weights = {}
  mtaufin_weights = {}
  eefin_weights = {}
  emufin_weights = {}
  etaufin_weights = {}
  for hdf in hd5list:
    #print count
    #print 'Count:',count
    hdf_tabs[count]=tables.File(hdf)
    #print 'Count:',count
              
#    for litem in hdf_tabs[count].walkGroups("/"):
#      for larr in hdf_tabs[count].listNodes(litem):
#        if(not(('weight' in str(larr)) or ('I3Index' in str(larr)))):
#          if(not(larr.name in tab_vals)):
#            print 'La'
#            tab_vals[larr.name] = larr  
#            tab_desc[larr.name] = larr.description  
#          else:
#            print 'Le'
#            tab_vals[larr.name].append(larr)
#          tab_vals[larr.name].flush()
#Event Info
    t_NeutEnergy = hdf_tabs[count].root.trueNeutrino.cols.energy[:]
    t_NeutZenith = hdf_tabs[count].root.trueNeutrino.cols.zenith[:]
    t_NeutType = hdf_tabs[count].root.trueNeutrino.cols.type[:]

#    t_NeutEnergy = hdf_tabs[count].root.MCNeutrino.cols.energy[:]
#    t_NeutZenith = np.cos(hdf_tabs[count].root.MCNeutrino.cols.zenith[:])
#    t_NeutType = hdf_tabs[count].root.MCNeutrino.cols.type[:]

#Weights
    for ene,zen,type in zip(t_NeutEnergy,np.cos(t_NeutZenith),t_NeutType):
      #print counter,ene,zen,type
      counter+=1
      meSQUIDSDict,mmSQUIDSDict,mtSQUIDSDict,eeSQUIDSDict,emSQUIDSDict,etSQUIDSDict = create_spline(type,ene,my_mutaus,my_tautaus,my_zens)
      for i,j in meSQUIDSDict.iteritems():
        if(i in mefin_weights):
          #print 'Others',zen,float(j(zen))
          #print 'Others Mu',zen,float(mmSQUIDSDict[i](zen))
          mefin_weights[i].append(float(j(zen)))
          mmufin_weights[i].append(float(mmSQUIDSDict[i](zen)))
          mtaufin_weights[i].append(float(mtSQUIDSDict[i](zen)))
          eefin_weights[i].append(float(eeSQUIDSDict[i](zen)))
          emufin_weights[i].append(float(emSQUIDSDict[i](zen)))
          etaufin_weights[i].append(float(etSQUIDSDict[i](zen)))
        else:
          #print 'First',zen,float(j(zen))
          #print 'First Mu',zen,float(mmSQUIDSDict[i](zen))
          mefin_weights[i] = []
          mmufin_weights[i] = []
          mtaufin_weights[i] = []
          eefin_weights[i] = []
          emufin_weights[i] = []
          etaufin_weights[i] = []
          mefin_weights[i].append(float(j(zen)))
          mmufin_weights[i].append(float(mmSQUIDSDict[i](zen)))
          mtaufin_weights[i].append(float(mtSQUIDSDict[i](zen)))
          eefin_weights[i].append(float(eeSQUIDSDict[i](zen)))
          emufin_weights[i].append(float(emSQUIDSDict[i](zen)))
          etaufin_weights[i].append(float(etSQUIDSDict[i](zen)))
        #print 'Weights:',i,efin_weights[i],mufin_weights[i]
        #print 'E Spline Value:',ene,zen,type,i,j([p-.002 for p in my_zens[:]])
        #print 'M Spline Value:',ene,zen,type,i,mSQUIDSDict[i]([p-.002 for p in my_zens[:]])

    hdf_tabs[count].close()
    count+=1
#  for i,j in tab_vals.iteritems():
#    fin_out.createTable("/ATT",i,tab_desc[i])
#    print i
  for i,j in meSQUIDSDict.iteritems():
    mmwn_var = 'mmu_weight['+str(i[0])+']['+str(i[1])+']'
    mewn_var = 'me_weight['+str(i[0])+']['+str(i[1])+']'
    mtwn_var = 'mtau_weight['+str(i[0])+']['+str(i[1])+']'
    emwn_var = 'emu_weight['+str(i[0])+']['+str(i[1])+']'
    eewn_var = 'ee_weight['+str(i[0])+']['+str(i[1])+']'
    etwn_var = 'etau_weight['+str(i[0])+']['+str(i[1])+']'
    #print mufin_weights[i][:100],efin_weights[i][:100]
    fin_out.createArray('/',mmwn_var,mmufin_weights[i])
    fin_out.createArray('/',mewn_var,mefin_weights[i])
    fin_out.createArray('/',mtwn_var,mtaufin_weights[i])
    fin_out.createArray('/',emwn_var,emufin_weights[i])
    fin_out.createArray('/',eewn_var,eefin_weights[i])
    fin_out.createArray('/',etwn_var,etaufin_weights[i])
  fin_out.close()

addWeights(my_mutaus,my_tautaus)

