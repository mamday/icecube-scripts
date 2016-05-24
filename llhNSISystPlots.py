#!/usr/bin/env python
import cPickle as pickle
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import glob
import sys,numpy,pylab
file_list = glob.glob(sys.argv[1])
llh_dict = {}
crmufrac_dict = {}
domeff_dict = {}
gamma_dict = {}
holeice_dict = {}
norm_dict = {}
norme_dict = {}

print len(file_list)
for lfile in file_list:
  try:
    llh_file = pickle.load(open(lfile, "rb"))
    mt = float("%.3f" % llh_file['result']['mt'])
    tt = float("%.5f" % llh_file['result']['tt'])
    llh_dict[(mt,tt)] = llh_file['result']['llh']
    crmufrac_dict[(mt,tt)] = llh_file['result']['atmmu_fraction']
    domeff_dict[(mt,tt)] = llh_file['result']['domeff']
    gamma_dict[(mt,tt)] = llh_file['result']['gamma']
    holeice_dict[(mt,tt)] = llh_file['result']['hole_ice']
    norm_dict[(mt,tt)] = llh_file['result']['norm']
    norme_dict[(mt,tt)] = llh_file['result']['norm_e']
  except:
    print lfile
my_mts = numpy.linspace(-0.015,0.015,11)
my_tts = numpy.linspace(-0.1,0.1,21)

#Fill llh arrays
crmufrac_arr = numpy.empty([len(my_tts),len(my_mts)]) 
domeff_arr = numpy.empty([len(my_tts),len(my_mts)]) 
gamma_arr = numpy.empty([len(my_tts),len(my_mts)]) 
holeice_arr = numpy.empty([len(my_tts),len(my_mts)]) 
norm_arr = numpy.empty([len(my_tts),len(my_mts)]) 
norme_arr = numpy.empty([len(my_tts),len(my_mts)]) 
eps_arr = numpy.empty([len(my_tts),len(my_mts)])
epst_arr = numpy.empty([len(my_tts),len(my_mts)])
epsf_arr = numpy.empty([len(my_tts),len(my_mts)])
countm = -1
countt = -1 

for mt in my_mts:
  countt+=1
  countm=-1
  for tt in my_tts:
    countm+=1
    mt = float("%.5f" % mt)
    tt = float("%.5f" % tt)
    #print mt,tt 
    if((mt,tt) in llh_dict.keys()):
      #print mt,tt,llh_dict[(mt,tt)]
      #print mt,tt,min(llh_dict, key=llh_dict.get),llh_dict[(mt,tt)],llh_dict[min(llh_dict, key=llh_dict.get)],(llh_dict[(mt,tt)]-llh_dict[min(llh_dict, key=llh_dict.get)])
      crmufrac_arr[countm][countt] = crmufrac_dict[(mt,tt)] 
      domeff_arr[countm][countt] = domeff_dict[(mt,tt)] 
      gamma_arr[countm][countt] = gamma_dict[(mt,tt)] 
      norm_arr[countm][countt] = norm_dict[(mt,tt)] 
      norme_arr[countm][countt] = norme_dict[(mt,tt)] 
      holeice_arr[countm][countt] = holeice_dict[(mt,tt)] 
      epst_arr[countm][countt] = (llh_dict[(mt,tt)]-llh_dict[min(llh_dict, key=llh_dict.get)]) 

#Plot?
from matplotlib import rcParams
from matplotlib import colors, ticker, cm
X, Y = numpy.meshgrid(my_mts, my_tts)
def makeBase(llh_dict,epst_arr):
  CS1 = plt.contour(X,Y,epst_arr, [1.15],colors=['r'])
  CS2 = plt.contour(X,Y,epst_arr, [2.3],colors=['k'])
#CS = plt.contour(X,Y,epst_arr, [5.99],colors=['r'])
#pylab.ylim(-.05,.05)
  pylab.rc('font', family='serif', size=14)
  pylab.xlabel(r'$\epsilon_{\mu \tau}$', size=30)
  pylab.ylabel(r'$\epsilon^{\prime}$', size=30)
  plt.plot([sys.argv[2]], [sys.argv[3]], 'k.', markersize=14.0)
  plt.plot([min(llh_dict, key=llh_dict.get)[0]], [min(llh_dict, key=llh_dict.get)[1]], 'm.', markersize=10.0)
#plt.clabel(CS, inline=1, fontsize=10)
#label = ['95%']
  label1 = ['68%']
  label2 = ['90%']
  for i in range(len(label1)):
      CS1.collections[i].set_label(label1[i])
      CS2.collections[i].set_label(label2[i])
#    CS.collections[i].set_label(label[i])
    
  pylab.legend(ncol=2)
  pylab.tight_layout()
import math
makeBase(llh_dict,epst_arr)
cs = plt.contourf(X, Y, crmufrac_arr, cmap=cm.PuBu_r,vmin=0.0,vmax=0.1,levels=numpy.linspace(0.0,0.1,10),extend='both')
cbar = plt.colorbar(cs)
cbar.set_clim(0.0,0.1)
cb_lim = cbar.get_clim()
print cb_lim
cb_frac = (0.05-cb_lim[0])/(cb_lim[1]-cb_lim[0])
cax = cbar.ax
cax.hlines([cb_frac], 0, [20], colors = 'r', linewidth = 5, linestyles = ':')
#pylab.savefig("PrelimNSISys-Reco.pdf")
pylab.savefig("NFit.pdf")
pylab.close()
makeBase(llh_dict,epst_arr)
cs = plt.contourf(X, Y, domeff_arr, cmap=cm.PuBu_r,vmin=0.7,vmax=1.3,levels=numpy.linspace(0.7,1.3,10),extend='both')
cbar = plt.colorbar(cs)
cbar.set_clim(0.7,1.3)
cb_lim = cbar.get_clim()
print cb_lim
cb_frac = (1.0-cb_lim[0])/(cb_lim[1]-cb_lim[0])
cax = cbar.ax
cax.hlines([cb_frac], 0, [20], colors = 'r', linewidth = 5, linestyles = ':')
pylab.savefig("NFit1.pdf")
pylab.close()
makeBase(llh_dict,epst_arr)
cs = plt.contourf(X, Y, holeice_arr, cmap=cm.PuBu_r,vmin=0.005,vmax=0.04,levels=numpy.linspace(0.005,0.04,10),extend='both')
cbar = plt.colorbar(cs)
cbar.set_clim(0.005,0.04)
cb_lim = cbar.get_clim()
print cb_lim
cb_frac = (0.02-cb_lim[0])/(cb_lim[1]-cb_lim[0])
cax = cbar.ax
cax.hlines([cb_frac], 0, [20], colors = 'r', linewidth = 5, linestyles = ':')
pylab.savefig("NFit2.pdf")
pylab.close()
makeBase(llh_dict,epst_arr)
cs = plt.contourf(X, Y, norm_arr, cmap=cm.PuBu_r,vmin=0.99,vmax=1.01,levels=numpy.linspace(0.99,1.01,10),extend='both')
cbar = plt.colorbar(cs)
cbar.set_clim(0.99,1.01)
cb_lim = cbar.get_clim()
print cb_lim
cb_frac = (1.0-cb_lim[0])/(cb_lim[1]-cb_lim[0])
cax = cbar.ax
cax.hlines([cb_frac], 0, [20], colors = 'r', linewidth = 5, linestyles = ':')
pylab.savefig("NFit3.pdf")
pylab.close()
makeBase(llh_dict,epst_arr)
cs = plt.contourf(X, Y, gamma_arr, cmap=cm.PuBu_r,vmin=-0.1,vmax=0.1,levels=numpy.linspace(-0.1,0.1,10),extend='both')
cbar = plt.colorbar(cs)
cbar.set_clim(-0.1,0.1)
cb_lim = cbar.get_clim()
print cb_lim
cb_frac = (0.0-cb_lim[0])/(cb_lim[1]-cb_lim[0])
cax = cbar.ax
cax.hlines([cb_frac], 0, [20], colors = 'r', linewidth = 5, linestyles = ':')
pylab.savefig("NFit4.pdf")
pylab.close()
makeBase(llh_dict,epst_arr)
cs = plt.contourf(X, Y, norme_arr, cmap=cm.PuBu_r,vmin=0.9,vmax=1.1,levels=numpy.linspace(0.9,1.1,10),extend='both')
cbar = plt.colorbar(cs)
cbar.set_clim(0.9,1.1)
cb_lim = cbar.get_clim()
print cb_lim
cb_frac = (1.0-cb_lim[0])/(cb_lim[1]-cb_lim[0])
cax = cbar.ax
cax.hlines([cb_frac], 0, [20], colors = 'r', linewidth = 5, linestyles = ':')
pylab.savefig("NFit5.pdf")
