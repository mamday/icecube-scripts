import icecube
from icecube import dataio,dataclasses,icetray
import glob,sys
import numpy
import cPickle as pickle

in_list = glob.glob(sys.argv[1])
my_pick = pickle.load(open(sys.argv[2],'rb'))

def i3Counts(file_name,evt_dict):
  in_file = dataio.I3File(file_name)
  #frame = in_file.pop_physics()
  evt_dict['reco_energy']=[]
  evt_dict['reco_zenith']=[]
  count = 0
  evt_id = -9
  sub_evt_id = -9
  run_id=-9
  while(in_file.more()):
      count+=1
      frame = in_file.pop_frame()
      if(not("SANTA_Fit_Muon" in frame.keys())):
        evt_id = frame["I3EventHeader"].event_id
        sub_evt_id = frame["I3EventHeader"].sub_event_id
        run_id = frame["I3EventHeader"].run_id
      else:
        m_energy = frame["SANTA_Fit_Muon"].energy
        m_zenith = frame["SANTA_Fit_Muon"].dir.zenith
     # m_energy = frame["SANTA_Muon"].energy
     # m_zenith = frame["SANTA_Muon"].dir.zenith
     # c_energy = frame["SANTA_Cascade"].energy
        c_energy = frame["SANTA_Fit_CascadeHad"].energy
        tot_energy = m_energy+c_energy
      #print count,tot_energy,m_zenith
        evt_dict['reco_energy'].append(tot_energy) 
        evt_dict['reco_zenith'].append(m_zenith) 
        if(tot_energy in my_pick['reco_energy']):
          print (run_id,evt_id,sub_evt_id)
      #evt_dict[(run_id,evt_id,sub_evt_id)]=(m_zenith,tot_energy)
      #if(sub_evt_id>0):
      #print sub_evt_id,evt_id,run_id

for f in in_list:
  a_dict={}
  print f
  i3Counts(f,a_dict)
  #print 'Events:',len(a_dict['reco_energy'])

  #print 'Compare',len(my_pick['reco_energy']),len([i for i in a_dict['reco_energy'] if i in my_pick['reco_energy']])
