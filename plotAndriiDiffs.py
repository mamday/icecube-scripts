import matplotlib
matplotlib.use('Agg')
import pylab,glob,sys,numpy
import cPickle as pickle

in_list = glob.glob(sys.argv[1]) 
print len(in_list)
dm2_list = numpy.zeros(len(in_list))
hi_list = numpy.zeros(len(in_list))
for ind,ifile in enumerate(in_list):
  pick_file = pickle.load(open(ifile,'rb'))
  dm2_list[ind] = pick_file['result']['dm31']
  hi_list[ind] = pick_file['result']['hole_ice']

dmbins = numpy.linspace(dm2_list.min(),dm2_list.max(),30)
counts,bins,patches = pylab.hist(dm2_list,bins=dmbins,histtype='step',color='k')
pylab.grid()
pylab.ylim(0,max(counts)+10)
pylab.savefig('AndriiCutAddDM2.png')
pylab.close()
hibins = numpy.linspace(hi_list.min(),hi_list.max(),30)
counts,bins,patches = pylab.hist(hi_list,bins=hibins,histtype='step',color='k')
pylab.ylim(0,max(counts)+10)
pylab.grid()
pylab.savefig('AndriiCutAddHI.png')
pylab.close()

