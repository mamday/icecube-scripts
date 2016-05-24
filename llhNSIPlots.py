#!/usr/bin/env python
import cPickle as pickle
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import glob
import sys,numpy,pylab
file_list = glob.glob(sys.argv[1])
llh_dict = {}
for lfile in file_list:
  try:
    llh_file = pickle.load(open(lfile, "rb"))
    mt = float("%.3f" % llh_file['result']['mt'])
    tt = float("%.5f" % llh_file['result']['tt'])
    llh_dict[(mt,tt)] = llh_file['result']['llh']
  except:
    print lfile
my_mts = numpy.linspace(-0.015,0.015,21)
my_tts = numpy.linspace(-0.1,0.1,21)

#Fill llh arrays
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
    mt = float("%.3f" % mt)
    tt = float("%.5f" % tt)
    print mt,tt 
    if((mt,tt) in llh_dict.keys()):
      print mt,tt,llh_dict[(mt,tt)]
      print mt,tt,min(llh_dict, key=llh_dict.get),llh_dict[(mt,tt)],llh_dict[min(llh_dict, key=llh_dict.get)],(llh_dict[(mt,tt)]-llh_dict[min(llh_dict, key=llh_dict.get)])
      epst_arr[countm][countt] = (llh_dict[(mt,tt)]-llh_dict[min(llh_dict, key=llh_dict.get)]) 

#Plot?
from matplotlib import rcParams
X, Y = numpy.meshgrid(my_mts, my_tts)
CS1 = plt.contour(X,Y,epst_arr, [1.15],colors=['b'])
CS2 = plt.contour(X,Y,epst_arr, [2.3],colors=['g'])
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
#pylab.savefig("PrelimNSISys-Reco.pdf")
pylab.savefig("NFit.pdf")

