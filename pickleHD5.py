import cPickle as pickle
import numpy,h5py
import glob,sys

in_file = glob.glob(sys.argv[1])
d_bool = sys.argv[2]
old_bool = sys.argv[3]

if(int(d_bool)==1):
  mc_string = 'data'
else:
  mc_string = 'genie'

for file in in_file:
  print file,int(d_bool)
  in_name = file[file.index(mc_string):file.index('.hd5')]
  h5file = h5py.File(file,'r')
  if(len(h5file.keys())==1):
    continue
  if(int(d_bool)==1):
    if(old_bool=='old'):
      casc_ene = h5file["SANTA_Cascade"]["energy"]
      muon_ene = h5file["SANTA_Muon"]["energy"]
      casc_zen = h5file["SANTA_Cascade"]["zenith"]
      muon_zen = h5file["SANTA_Muon"]["zenith"]
    else:
      casc_ene = h5file["SANTA_Fit_CascadeHad"]["energy"]
      muon_ene = h5file["SANTA_Fit_Muon"]["energy"]
      casc_zen = h5file["SANTA_Fit_CascadeHad"]["zenith"]
      muon_zen = h5file["SANTA_Fit_Muon"]["zenith"]
    tot_dict = {}
    tot_dict['reco_energy'] = muon_ene + casc_ene
    tot_dict['reco_zenith'] = muon_zen
    tot_dict['reco_cascade'] = casc_ene
    tot_dict['reco_track'] = muon_ene
    pickle.dump(tot_dict, open('/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/Pickles/'+in_name+'.pckl',"wb"))
  else:
    if(old_bool=='old'):
      casc_ene = h5file["SANTA_Cascade"]["energy"]
      muon_ene = h5file["SANTA_Muon"]["energy"]
      casc_zen = h5file["SANTA_Cascade"]["zenith"]
      muon_zen = h5file["SANTA_Muon"]["zenith"]
    else:
      casc_ene = h5file["SANTA_Fit_CascadeHad"]["energy"]
      muon_ene = h5file["SANTA_Fit_Muon"]["energy"]
      casc_zen = h5file["SANTA_Fit_CascadeHad"]["zenith"]
      muon_zen = h5file["SANTA_Fit_Muon"]["zenith"]
    tneut_ene = h5file["trueNeutrino"]["energy"]
    tneut_zen = h5file["trueNeutrino"]["zenith"]
    tneut_ptype = h5file["trueNeutrino"]["type"]
    int_type = h5file["I3MCWeightDict"]["InteractionType"]
    eWeight = h5file["UnOscWeightNuE"]["value"]    
    mWeight = h5file["UnOscWeightNuMu"]["value"]    
    cc_dict = {}
    nc_dict = {}
    cc_dict['energy'] = tneut_ene[int_type==1]
    cc_dict['zenith'] = tneut_zen[int_type==1]
    cc_dict['reco_energy'] = muon_ene[int_type==1]+casc_ene[int_type==1]
    cc_dict['reco_zenith'] = muon_zen[int_type==1]
    cc_dict['reco_track'] = muon_ene[int_type==1]
    cc_dict['reco_cascade'] = casc_ene[int_type==1]
    cc_dict['weight_e'] = eWeight[int_type==1]
    cc_dict['weight_mu'] = mWeight[int_type==1]
    cc_dict['ptype'] = tneut_ptype[int_type==1]

    nc_dict['energy'] = tneut_ene[int_type==2]
    nc_dict['zenith'] = tneut_zen[int_type==2]
    nc_dict['reco_energy'] = muon_ene[int_type==2]+casc_ene[int_type==2]
    nc_dict['reco_zenith'] = muon_zen[int_type==2]
    nc_dict['reco_track'] = muon_ene[int_type==2]
    nc_dict['reco_cascade'] = casc_ene[int_type==2]
    nc_dict['weight_e'] = eWeight[int_type==2]
    nc_dict['weight_mu'] = mWeight[int_type==2]
    nc_dict['ptype'] = tneut_ptype[int_type==2]

    tot_dict = {}
    tot_dict['CC']=cc_dict
    tot_dict['NC']=nc_dict
    pickle.dump(tot_dict, open('/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/HD5Files/Pickles/'+in_name+'.pckl',"wb"))

