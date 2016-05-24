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
  llh_file = pickle.load(open(lfile, "rb"))
  fs = llh_file['result']['fit_stat']
  th23 = float("%.3f" % llh_file['result']['theta23'])
  dm2 = float("%.5f" % llh_file['result']['dm31'])
  if(not(fs=='Suceeded')):
    print 'Fail',th23,dm2
    llh_dict[(th23,dm2)] = False 
  else:
    llh_dict[(th23,dm2)] = llh_file['result']['llh']
  #print lfile,th23,dm2,llh_file['result']['llh']
  #if(llh_file['result']['llh']<-99000):
  #  print 'Aha!',lfile
  #print th23,dm2,llh_dict[(th23,dm2)] 
my_th23s = numpy.linspace(0.4,1.2,51)
my_dm2s = numpy.linspace(0.002,0.004,51)
#print my_th23s
#print my_dm2s
#Fill llh arrays
prof_arr = numpy.empty([len(my_th23s),len(my_dm2s)])
epst_arr = numpy.empty([len(my_th23s),len(my_dm2s)])
epsf_arr = numpy.empty([len(my_th23s),len(my_dm2s)])
countm = -1
countt = -1 
for th23 in my_th23s:
  countt+=1
  countm=-1
  for dm2 in my_dm2s:
    countm+=1
    th23 = float("%.3f" % th23)
    dm2 = float("%.5f" % dm2)
    if((th23,dm2) in llh_dict):
      if(llh_dict[(th23,dm2)]):
        print th23,dm2,llh_dict[(th23,dm2)]
        print th23,dm2,min(llh_dict, key=llh_dict.get),llh_dict[(th23,dm2)],llh_dict[min(llh_dict, key=llh_dict.get)],(llh_dict[(th23,dm2)]-llh_dict[min(llh_dict, key=llh_dict.get)])
        epst_arr[countm][countt] = (llh_dict[(th23,dm2)]-llh_dict[min(llh_dict, key=llh_dict.get)]) 
        prof_arr[countt][countm] = llh_dict[(th23,dm2)] 
      else:
        print 'This',th23,dm2
        print th23,dm2,min(llh_dict, key=llh_dict.get),epst_arr[countm-1][countt],llh_dict[min(llh_dict, key=llh_dict.get)]
        epst_arr[countm][countt] = epst_arr[countm-1][countt] 
prof_count = 0
prof_th23 = []
for th23_list in prof_arr:
  #print 'Melanie Test',min(th23_list),my_th23s[prof_count]
  prof_th23.append(min(th23_list))
  prof_count+=1
#print 'Last Melanie Test',min(prof_th23),[i-min(prof_th23) for i in prof_th23]
fig = pylab.figure()
pylab.plot([numpy.sin(i)**2 for i in my_th23s],[2*(i-min(prof_th23)) for i in prof_th23],color='k')
pylab.xlabel("r'$Sin^2(\theta_{23})$'")
pylab.ylabel(r'2*$\Delta (LLH)$')
pylab.xlim(0.25,0.75)
pylab.ylim(0.0,4.0)
fig.set_size_inches(7,2)
pylab.grid()
pylab.savefig('LLHProfTh23.pdf')
pylab.close()
#Plot?
from matplotlib import rcParams
my_s2th23s = numpy.cos(my_th23s)**2
my_1000dm2s = 1000*my_dm2s 
X, Y = numpy.meshgrid(my_s2th23s, my_1000dm2s)
CS1 = plt.contour(X,Y,epst_arr, [1.15],colors=['b'])
CS2 = plt.contour(X,Y,epst_arr, [2.3],colors=['g'])
#CS = plt.contour(X,Y,epst_arr, [5.99],colors=['r'])
#pylab.ylim(-.05,.05)
pylab.rc('font', family='serif', size=14)
pylab.xlabel(r'$sin^2(\theta_{23})$', size=30)
pylab.ylabel(r'$\Delta m^2_{32} (10^{-3} eV^{2})$', size=30)
plt.yticks(numpy.arange(min(my_1000dm2s), max(my_1000dm2s)+1, 0.2))
#plt.plot([sys.argv[2]], [sys.argv[3]], 'k.', markersize=14.0)
plt.plot([numpy.sin(min(llh_dict, key=llh_dict.get)[0])**2], [1000*min(llh_dict, key=llh_dict.get)[1]], 'm.', markersize=10.0)
plt.grid(True,linestyle='--')
#plt.clabel(CS, inline=1, fontsize=10)
#label = ['95%']
label1 = ['68%']
label2 = ['90%']
for i in range(len(label1)):
    CS1.collections[i].set_label(label1[i])
    CS2.collections[i].set_label(label2[i])
#    CS.collections[i].set_label(label[i])
pylab.xlim(0.25,0.75)    
pylab.legend(ncol=2)
pylab.tight_layout()
#pylab.savefig("PrelimNSISys-Reco.pdf")
pylab.savefig("OFit.pdf")

