import icecube
from icecube import dataio,dataclasses,icetray
import glob,sys
import numpy
import cPickle as pickle

in_list = glob.glob(sys.argv[1])
in_text = sys.argv[2]

def textCounts(file_name,evt_dict):
  my_file = open(file_name)
  count = 0
  for line in my_file.readlines():
    tup_parts = line.split(',') 
    first = float(tup_parts[0][1:])
    sec = float(tup_parts[1])
    third = float(tup_parts[2][:-2])
    if(third>0):
      count+=1
    evt_dict[(first,sec,third)]=1
  #print 'Num >0',count

def i3Counts(file_name,evt_dict):
  in_file = dataio.I3File(file_name)
  #frame = in_file.pop_physics()
  #evt_dict['reco_energy']=[]
  #evt_dict['reco_zenith']=[]
  count = 0
  frame = in_file.pop_daq()
  while(in_file.more()):
      count+=1
      evt_id = frame["I3EventHeader"].event_id
      sub_evt_id = frame["I3EventHeader"].sub_event_id
      run_id = frame["I3EventHeader"].run_id
      #m_energy = frame["SANTA_Fit_Muon"].energy
      #m_zenith = frame["SANTA_Fit_Muon"].dir.zenith
      #m_energy = frame["SANTA_Muon"].energy
      #m_zenith = frame["SANTA_Muon"].dir.zenith
      #c_energy = frame["SANTA_Cascade"].energy
      #tot_energy = m_energy+c_energy
      #print count,tot_energy,m_zenith
      #evt_dict['reco_energy'].append(tot_energy) 
      #evt_dict['reco_zenith'].append(m_zenith) 
      evt_dict[(run_id,evt_id,sub_evt_id)]=1
      #if(sub_evt_id>0):
      #  print sub_evt_id,evt_id,run_id
      frame = in_file.pop_daq()

t_dict={}
textCounts(in_text,t_dict)

for f in in_list:
  a_dict={}
  #print f
  i3Counts(f,a_dict)
  print 'Events:',len(t_dict),len(a_dict)
  for key,val in a_dict.iteritems():
    #print key
    if(key in t_dict):
       del t_dict[key]

print 'Events:',len(t_dict),len(a_dict)
