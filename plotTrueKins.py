import cPickle as pickle
import numpy
import matplotlib
matplotlib.use('Agg')
import pylab
import os,sys

p_file = sys.argv[1]
p_dicts = pickle.load(open(p_file,'rb'))

nc_dict = p_dicts['NC']
cc_dict = p_dicts['CC']

cc_ene = p_dicts['CC']['energy']
cc_zen = p_dicts['CC']['zenith']
cc_rene = p_dicts['CC']['reco_energy']
bcc_rzen = p_dicts['CC']['reco_zenith']
cc_rzen= bcc_rzen[(cc_ene>6) & (cc_ene<56)]
cc_mweight = 365*24*3600*p_dicts['CC']['weight_muj12']
ccosc_mweight = 365*24*3600*p_dicts['CC']['weight']
zcc_mweight = cc_mweight[(cc_ene>6) & (cc_ene<56)] 
zccosc_mweight = ccosc_mweight[(cc_ene>6) & (cc_ene<56)] 

#pylab.hist(cc_ene,bins=numpy.linspace(0,100,20),color='k',linestyle='solid',weights=cc_mweight,histtype='step',label='Unoscillated Truth')
#pylab.hist(cc_ene,bins=numpy.linspace(0,100,20),color='k',linestyle='dashed',weights=ccosc_mweight,histtype='step',label='Oscillated Truth')
pylab.hist(cc_rene,bins=numpy.linspace(6,56,9),color='k',linestyle='dashed',weights=cc_mweight,histtype='step',label='Unoscillated Reco')
pylab.hist(cc_rene,bins=numpy.linspace(6,56,9),color='k',linestyle='dashdot',weights=ccosc_mweight,histtype='step',label='Oscillated Reco')
pylab.xlabel("Energy (GeV)",fontsize=20)
pylab.ylabel("Events",fontsize=20)
pylab.xlim(6,56)
pylab.legend()
pylab.tight_layout()
pylab.savefig('CCEneHist.pdf')
pylab.close()

#pylab.hist(numpy.cos(cc_zen),bins=numpy.linspace(-1,1,20),color='k',linestyle='solid',weights=cc_mweight,histtype='step',label='Unoscillated Truth')
#pylab.hist(numpy.cos(cc_zen),bins=numpy.linspace(-1,1,20),color='k',linestyle='dashed',weights=ccosc_mweight,histtype='step',label='Oscillated Truth')
pylab.hist(numpy.cos(cc_rzen),bins=numpy.linspace(-1,1,9),color='k',linestyle='dashed',weights=zcc_mweight,histtype='step',label='Unoscillated Reco')
pylab.hist(numpy.cos(cc_rzen),bins=numpy.linspace(-1,1,9),color='k',linestyle='dashdot',weights=zccosc_mweight,histtype='step',label='Oscillated Reco')
pylab.xlabel("cos(Zenith)",fontsize=20)
pylab.ylabel("Events",fontsize=20)
pylab.legend()
pylab.tight_layout()
pylab.savefig('CCZenHist.pdf')
pylab.close()
