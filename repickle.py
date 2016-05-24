import cPickle as pickle
import sys,numpy

f_pickle = pickle.load(open(sys.argv[1],'rb'))
s_pickle = pickle.load(open(sys.argv[2],'rb'))

f_ene = f_pickle['reco_energy']
f_zen = f_pickle['reco_zenith']
sn_ene = numpy.array(s_pickle['reco_energy'])
sn_zen = numpy.array(s_pickle['reco_zenith'])
s_ene = sn_ene[(sn_ene>=6) & (sn_ene<=56) & (numpy.cos(sn_zen)<=0)]
s_zen = sn_zen[(sn_ene>=6) & (sn_ene<=56) & (numpy.cos(sn_zen)<=0)]
print len(f_ene),len(f_zen),len(s_ene),len(s_zen)
print len([ind for ind,i in enumerate(s_ene) if not(i in f_ene)]),len([i for i in s_zen if not(i in f_zen)]) 
new_ene = s_ene[[ind for ind,i in enumerate(s_ene) if not(i in f_ene)]]
new_zen = s_zen[[ind for ind,i in enumerate(s_ene) if not(i in f_ene)]]

my_dict = {}
my_dict['reco_energy']=new_ene
my_dict['reco_zenith']=new_zen

pickle.dump(my_dict,open('IC863Diff.pckl','wb'))

