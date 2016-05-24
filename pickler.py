import icecube
from icecube import dataio,dataclasses,icetray
import glob,sys
import numpy
import cPickle as pickle

if(len(sys.argv)==2):
  in_list = glob.glob(sys.argv[1])

def i3Counts(file_name,evt_dict):
  in_file = dataio.I3File(file_name)
  #frame = in_file.pop_physics()
  evt_dict['reco_energy']=[]
  evt_dict['reco_zenith']=[]
  count = 0
  while(in_file.more()):
      count+=1
      frame = in_file.pop_physics()
      evt_id = frame["I3EventHeader"].event_id
      sub_evt_id = frame["I3EventHeader"].sub_event_id
      run_id = frame["I3EventHeader"].run_id
      #m_energy = frame["SANTA_Fit_Muon"].energy
      #m_zenith = frame["SANTA_Fit_Muon"].dir.zenith
      hlc_z = frame["FirstHLCvertex"].pos.z
      m_energy = frame["SANTA_Muon"].energy
      m_zenith = frame["SANTA_Muon"].dir.zenith
      c_energy = frame["SANTA_Cascade"].energy
      tot_energy = m_energy+c_energy
      #print count,tot_energy,m_zenith
      if(hlc_z<-250):
        evt_dict['reco_energy'].append(tot_energy) 
        evt_dict['reco_zenith'].append(m_zenith) 
      #evt_dict[(run_id,evt_id,sub_evt_id)]=(m_zenith,tot_energy)
      #if(sub_evt_id>0):
      #print sub_evt_id,evt_id,run_id

for f in in_list:
  a_dict={}
  print f
  i3Counts(f,a_dict)
  print 'Events:',len(a_dict['reco_energy'])
  print 'Events:',len(a_dict['reco_energy'])
  if('genie' in f):
    fname = '/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/PRDPickles/'+f[f.find('genie'):f.find('.i3')] + '-Cut.pckl'
  elif('IC86' in f):
    fname = '/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/PRDPickles/'+f[f.find('IC86'):f.find('.i3')] + '-Cut.pckl'
  elif('PRD' in f):
    fname = '/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/PRDPickles/'+f[f.find('PRD'):f.find('.i3')] + '-Cut.pckl'
  print fname
  pickle.dump(a_dict,open(fname,'wb'))
