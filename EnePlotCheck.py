import cPickle as pickle
import numpy
from numpy import *
import sys,os

import matplotlib
matplotlib.use('Agg')
import pylab

e_bool = False
m_bool = False
t_bool = False
#Determine flavor of neutrino from name of input file
if('12' in sys.argv[1]):
  e_bool = True
elif('14' in sys.argv[1]):
  m_bool = True
elif('16' in sys.argv[1]):
  t_bool = True

#Functions for two neutrino weights
def propDist(zenith):
    L1 = 19.
    R = 6378.2 + L1
    phi = arcsin((1-L1/R)*sin(zenith))
    psi = zenith - phi
    return sqrt( (R-L1)**2 + R**2 - (2*(R-L1)*R*cos(psi)))

def TwoNeutProb(energy,zenith):
  numu_to_nutau = 0.99*sin(1.267*(0.00272)*propDist(zenith)/energy)**2

#Open files and determine if they were accidentally reprocessed or not
in_pick = pickle.load(open(sys.argv[1],'rb'))
bool_cc = in_pick['CC']['match_e']==True
bool_nc = in_pick['NC']['match_e']==True
set_num = sys.argv[1][sys.argv[1].find('ic.')+3:sys.argv[1].find('ic.')+7]
print set_num
#Get energies and angles for NC and CC interactions 
orig_ene_cc = in_pick['CC']['energy'][bool_cc] 
orig_ene_nc = in_pick['NC']['energy'][bool_nc] 
orig_zen_cc = in_pick['CC']['zenith'][bool_cc] 
orig_zen_nc = in_pick['NC']['zenith'][bool_nc] 

rep_ene_cc = in_pick['CC']['energy'][bool_cc==False] 
rep_ene_nc = in_pick['NC']['energy'][bool_nc==False] 
rep_zen_cc = in_pick['CC']['zenith'][bool_cc==False] 
rep_zen_nc = in_pick['NC']['zenith'][bool_nc==False]

#Get two neutrino oscillation probabilites for all the arrays
orig_osc_prob_cc = numpy.array([TwoNeutProb(i,j) for i,j in zip(orig_ene_cc,orig_zen_cc)])
orig_osc_prob_nc = numpy.array([TwoNeutProb(i,j) for i,j in zip(orig_ene_nc,orig_zen_nc)])
rep_osc_prob_cc = numpy.array([TwoNeutProb(i,j) for i,j in zip(rep_ene_cc,rep_zen_cc)])
rep_osc_prob_nc = numpy.array([TwoNeutProb(i,j) for i,j in zip(rep_ene_nc,rep_zen_nc)])

#Weights
if(e_bool):
  orig_weight_cc = in_pick['CC']['weight_ej12'][bool_cc] 
  orig_weight_nc = in_pick['NC']['weight_ej12'][bool_nc] 
  rep_weight_cc = in_pick['CC']['weight_ej12'][bool_cc] 
  rep_weight_nc = in_pick['NC']['weight_ej12'][bool_nc] 
elif(m_bool):
  orig_weight_cc = (1-orig_osc_prob_cc)*in_pick['CC']['weight_muj12'][bool_cc] 
  orig_weight_nc = (1-orig_osc_prob_nc)*in_pick['NC']['weight_muj12'][bool_nc] 
  rep_weight_cc = (1-rep_osc_prob_cc)*in_pick['CC']['weight_muj12'][bool_cc] 
  rep_weight_nc = (1-rep_osc_prob_nc)*in_pick['NC']['weight_muj12'][bool_nc] 
elif(t_bool):
  orig_weight_cc = orig_osc_prob_cc*in_pick['CC']['weight_muj12'][bool_cc] 
  orig_weight_nc = orig_osc_prob_nc*in_pick['NC']['weight_muj12'][bool_nc] 
  rep_weight_cc = rep_osc_prob_cc*in_pick['CC']['weight_muj12'][bool_cc] 
  rep_weight_nc = rep_osc_prob_nc*in_pick['NC']['weight_muj12'][bool_nc] 

ene_bins = numpy.linspace(0,200,9)
zen_bins = numpy.linspace(-1,0,9)

pylab.hist(orig_ene_cc,bins=ene_bins,weight=orig_weight_cc)
pylab.hist(rep_ene_cc,bins=ene_bins,weight=rep_weight_cc)
pylab.savefig('OriginalCCEne-%s.png' % set_num)
pylab.close()

pylab.hist(cos(orig_zen_cc),bins=zen_bins,weight=orig_weight_cc)
pylab.hist(cos(rep_zen_cc),bins=zen_bins,weight=rep_weight_cc)
pylab.savefig('OriginalCCZen-%s.png' % set_num)
pylab.close()

pylab.hist(orig_ene_nc,bins=ene_bins,weight=orig_weight_nc)
pylab.hist(rep_ene_nc,bins=ene_bins,weight=rep_weight_nc)
pylab.savefig('ReprocessNCEne-%s.png' % set_num)
pylab.close()

pylab.hist(cos(orig_zen_nc),bins=zen_bins,weight=orig_weight_nc)
pylab.hist(cos(rep_zen_nc),bins=zen_bins,weight=rep_weight_nc)
pylab.savefig('ReprocessNCZen-%s.png' % set_num)
pylab.close()

#print orig_weight_cc[:10],orig_weight_nc[:10],rep_weight_cc[:10],rep_weight_nc[:10] 
