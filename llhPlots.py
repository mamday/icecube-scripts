#!/usr/bin/env python

import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt

import sys,numpy,pylab
llh_file = open(sys.argv[1], "r")
llh_dict = {}
sys_dict = {}
for line in llh_file.readlines():
  c_split = line.split(',')
  if('Migrad' in c_split[0]):
    c_split[0] = c_split[0].split(' ')[1]
  llh_dict[(float(c_split[0]),float(c_split[1]))] = float(c_split[2])
  sys_dict[(float(c_split[0]),float(c_split[1]))] = (float(c_split[3]),float(c_split[6]),float(c_split[7]),float(c_split[8]),float(c_split[9]))

#print llh_dict, min(llh_dict, key=llh_dict.get), llh_dict[min(llh_dict, key=llh_dict.get)]


#Global variables
#my_mutaus = numpy.linspace(-0.015,0.015,31)
my_mutaus = numpy.linspace(-0.01,0.01,21)
my_tautaus = numpy.linspace(-0.1,0.1,21)

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
    mt = float("%.3f" % mt)
    tt = float("%.3f" % tt)
    if((mt,tt) in llh_dict.keys()):
      print mt,tt,min(llh_dict, key=llh_dict.get),llh_dict[(mt,tt)],llh_dict[min(llh_dict, key=llh_dict.get)],(llh_dict[(mt,tt)]-llh_dict[min(llh_dict, key=llh_dict.get)]),sys_dict[(mt,tt)]
      epst_arr[countm][countt] = 2*(llh_dict[(mt,tt)]-llh_dict[min(llh_dict, key=llh_dict.get)]) 
#        epsf_arr[countm][countt] = self.llhFunc(4,minuit_min.values['norm'],mt,tt,minuit_min.values['domeff'],minuit_min.values['holeice'],minuit_min.values['gamma'],minuit_min.values['norm_e'])-minuit_min.fval 

#Plot?
from matplotlib import rcParams
X, Y = numpy.meshgrid(my_mutaus, my_tautaus)
CS1 = plt.contour(X,Y,epst_arr, [2.3],colors=['b'])
CS2 = plt.contour(X,Y,epst_arr, [4.6],colors=['g'])
CS = plt.contour(X,Y,epst_arr, [5.99],colors=['r'])
#pylab.ylim(-.05,.05)
pylab.rc('font', family='serif', size=14)
pylab.xlabel(r'$\epsilon_{\mu \tau}$', size=30)
pylab.ylabel('$\\epsilon^{\\prime}$', size=30)
plt.plot([sys.argv[2]], [sys.argv[3]], 'k.', markersize=14.0)
plt.plot([min(llh_dict, key=llh_dict.get)[0]], [min(llh_dict, key=llh_dict.get)[1]], 'm.', markersize=14.0)
#plt.clabel(CS, inline=1, fontsize=10)
label = ['95%']
label1 = ['68%']
label2 = ['90%']
for i in range(len(label)):
    CS1.collections[i].set_label(label1[i])
    CS2.collections[i].set_label(label2[i])
    CS.collections[i].set_label(label[i])
    
pylab.legend(ncol=2)
pylab.tight_layout()
pylab.savefig("PrelimNSISys-Reco.pdf")

