#!/usr/bin/env python
import cPickle as pickle
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import glob
import sys,numpy,pylab
file_list = glob.glob(sys.argv[1])
mt_list = [] 
tt_list = [] 
for lfile in file_list:
  try:
    llh_file = pickle.load(open(lfile, "rb"))
    mt_list.append(float("%.3f" % llh_file['result']['mt']))
    tt_list.append(float("%.5f" % llh_file['result']['tt']))
  except:
    print lfile
my_bins =101 
counts,ybins,xbins,image = pylab.hist2d(mt_list,tt_list,range=[[-0.015,0.015],[-0.1,0.1]],weights=numpy.array([float(1)/float(350) for j in mt_list]),bins=my_bins)
print xbins,ybins,counts.shape
#counts,ybins,xbins,image = pylab.hist2d(mt_list,tt_list,bins=10)
pylab.colorbar()
#pylab.xlim(-0.015,0.015)
#pylab.ylim(-0.1,0.1)
new_counts = numpy.array([[float(-1) for i in xrange(my_bins)] for j in xrange(my_bins)])
for i in xrange(((my_bins-1)/2)+1):
  if(i>0):
    p = ((my_bins-1)/2)-i
    q = ((my_bins-1)/2)+(i+1)
    tot_counts = 0
#Calculate total counts so far
    for j in xrange(p,q): 
      for k in xrange(p,q): 
        tot_counts +=counts[j][k]
#Fill unfilled counts
    print i,p,q,tot_counts
    for j in xrange(p,q): 
      for k in xrange(p,q): 
        if(new_counts[j][k]==-1):
          new_counts[j][k] = tot_counts
  else:
    print i,((my_bins-1)/2),counts[((my_bins-1)/2)][((my_bins-1)/2)]
    new_counts[((my_bins-1)/2)][((my_bins-1)/2)] = counts[((my_bins-1)/2)][((my_bins-1)/2)]
print counts, new_counts
pylab.close()
from matplotlib import colors, ticker, cm
cs = plt.contourf(new_counts,extent=[-0.015,0.015,-0.1,0.1],cmap=cm.PuBu_r)
plt.colorbar(cs)
pylab.savefig("Braz.pdf")
