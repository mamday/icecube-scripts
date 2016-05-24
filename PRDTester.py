import icecube
from icecube import dataio,dataclasses,icetray
import glob,sys
import numpy
import cPickle as pickle

in_list = glob.glob(sys.argv[1])
in_pickle = pickle.load(open(sys.argv[2],'rb'))

def i3Counts(file_name,evt_dict,pick):
  in_file = dataio.I3File(file_name)
  #frame = in_file.pop_physics()
  while(in_file.more()):
      frame = in_file.pop_physics()
      evt_id = frame["I3EventHeader"].event_id
      sub_evt_id = frame["I3EventHeader"].sub_event_id
      run_id = frame["I3EventHeader"].run_id
      hlc_z = frame["FirstHLCvertex"].pos.z
      mm_energy = frame["SANTA_Muon"].energy
      mm_zenith = frame["SANTA_Muon"].dir.zenith
      mc_energy = frame["SANTA_Cascade"].energy
      tot_energy = mm_energy+mc_energy
      tn_energy = frame["trueNeutrino"].energy
      tn_zenith = frame["trueNeutrino"].dir.zenith
      #tm_energy = frame["trueMuon"].energy
      #tc_energy = frame["trueCascade"].energy
      #tmm_zenith = frame["trueMuon"].dir.zenith
#CC=1 NC =2
      int_type = frame["I3MCWeightDict"]["InteractionType"]
      p_tenergy = 0
      p_nenergy = 0
      pte_ind = -1
      pne_ind = -2
      if(int_type==1):
        p_tenergy=list(pick['CC']['reco_energy']) 
        p_nenergy=list(pick['CC']['energy']) 
        if(tot_energy in p_tenergy):
          pte_ind = p_tenergy.index(tot_energy) 
        if(tn_energy in p_nenergy):
          pne_ind = p_nenergy.index(tn_energy) 
      if(int_type==2):
        p_tenergy=list(pick['NC']['reco_energy']) 
        p_nenergy=list(pick['NC']['energy']) 
        if(tot_energy in p_tenergy):
          pte_ind = p_tenergy.index(tot_energy) 
        #ptz_ind = p_tzen.index(mm_zenith) 
        if(tn_energy in p_nenergy):
          pne_ind = p_nenergy.index(tn_energy) 
        #pnz_ind = p_nenergy.index(tn_zenith) 
      #print 'Check Inds',pte_ind==pne_ind 
      #if((pte_ind==pne_ind) and hlc_z<-250):
      #if((pte_ind==pne_ind) and hlc_z<-250):
      if((pne_ind>0)):
        m_bool = (pte_ind==pne_ind)
        if(int_type==1):
          if(not(m_bool)):
            print pick['CC']['reco_energy'][pne_ind]-tot_energy
          evt_dict['CC']['match_e'].append(m_bool) 
          evt_dict['CC']['vtxz'].append(hlc_z) 
        if(int_type==2):
          if(not(m_bool)):
            print pick['NC']['reco_energy'][pne_ind]-tot_energy
          evt_dict['NC']['match_e'].append(m_bool) 
          evt_dict['NC']['vtxz'].append(hlc_z) 
        for key in pick['NC'].keys():
          if(int_type==1):
            evt_dict['CC'][key].append(pick['CC'][key][pne_ind])
          if(int_type==2):
            evt_dict['NC'][key].append(pick['NC'][key][pne_ind])


a_dict={}
a_dict['CC']={}  
a_dict['NC']={}
a_dict['CC']['match_e']=[]
a_dict['CC']['vtxz']=[]
a_dict['NC']['match_e']=[]
a_dict['NC']['vtxz']=[]
for key in in_pickle['NC'].keys():
  a_dict['CC'][key]=[]
  a_dict['NC'][key]=[]

for f in in_list:
  #print f
  i3Counts(f,a_dict,in_pickle)
#  print 'CC Events:',len(a_dict['CC']['reco_energy'])
#  print 'NC Events:',len(a_dict['NC']['reco_energy'])

for key in a_dict['NC'].keys():
  a_dict['CC'][key]=numpy.array(a_dict['CC'][key]) 
  a_dict['NC'][key]=numpy.array(a_dict['NC'][key]) 

if('genie' in f):
  fname = '/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/PRDPickles/'+f[f.find('genie'):f.find('genie')+13] + '-SaveCut.pckl'
elif('Level2' in f):
  fname = '/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/PRDPickles/'+f[f.find('Level2'):f.find('.i3')] + '-SaveCut.pckl'
print fname
pickle.dump(a_dict,open(fname,'wb'))

