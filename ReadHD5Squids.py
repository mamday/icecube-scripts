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

file = sys.argv[1]

ene = float(sys.argv[2]) 
zen = float(sys.argv[3]) 

def make_squids():
  file_name = file 
  nuSQ = nsq.nuSQUIDSAtm(file_name)

#Neutrinos
  print "NuToTau",ene,zen,nuSQ.EvalFlavor(2,zen,ene*nuSQ.units.GeV,0)
  print "NuToMu",ene,zen,nuSQ.EvalFlavor(1,zen,ene*nuSQ.units.GeV,0)
  print "NuToE",ene,zen,nuSQ.EvalFlavor(0,zen,ene*nuSQ.units.GeV,0)

#Anti-Neutrinos
  print "NuBartoTau",ene,zen,nuSQ.EvalFlavor(2,zen,ene*nuSQ.units.GeV,1)
  print "NuBarToMu",ene,zen,nuSQ.EvalFlavor(1,zen,ene*nuSQ.units.GeV,1)
  print "NuBarToE",ene,zen,nuSQ.EvalFlavor(0,zen,ene*nuSQ.units.GeV,1)

make_squids()


