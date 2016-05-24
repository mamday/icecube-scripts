import icecube
from icecube import dataio,dataclasses,icetray
import glob,sys
import cPickle as pickle

if(len(sys.argv)==2):
  in_list = glob.glob(sys.argv[1])
else:
  in_list = sys.argv[1:]
print in_list
def i3Counts(file_name,evt_dict):
  in_file = dataio.I3File(file_name)
  count=0
  frame = in_file.pop_physics()
  while(in_file.more()):
      evt_id = frame["I3EventHeader"].event_id
      sub_evt_id = frame["I3EventHeader"].sub_event_id
      run_id = frame["I3EventHeader"].run_id
      m_energy = frame["SANTA_Fit_Muon"].energy
      m_zenith = frame["SANTA_Fit_Muon"].dir.zenith
      c_energy = frame["SANTA_Fit_CascadeHad"].energy
      tot_energy = m_energy+c_energy
      evt_dict[(run_id,evt_id,sub_evt_id)]=(m_zenith,tot_energy)
      #if(sub_evt_id>0):
      #print sub_evt_id,evt_id,run_id
      count+=1
      frame = in_file.pop_physics()

a_dict={}
for f in in_list[:3]:
  print f
  i3Counts(f,a_dict)
  print len(a_dict),a_dict

j_dict={}
for f in in_list[3:]:
  print f
  i3Counts(f,j_dict)
  print len(j_dict)
count = 0

for key,val in j_dict.iteritems():
  if(key in a_dict):
    print key
    count+=1

print 'CombTot:',count
