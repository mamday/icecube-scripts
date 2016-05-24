import h5py
import sys
from glob import glob

infiles = glob(sys.argv[1]) 

def out_name(fname,gname):
  if len(sys.argv)==5:
    f_string = sys.argv[3]
    l_string = sys.argv[4]
    f_ind = fname.find(f_string)+len(f_string)
    l_ind = fname.find(l_string)
    outname = gname+fname[f_ind:l_ind]
  else:
    print 'Four input arguments not given. Instead given: ',len(sys.argv)
    outname = gname

  return outname

for fname in infiles:
  in_file = h5py.h5f.open(fname, h5py.h5f.ACC_RDONLY)
  root_id = h5py.h5g.open(in_file,"/")
  print fname

  for gname in root_id:
    if(('NuMu' in gname) and not('Bar' in gname)):
      group_id = h5py.h5g.open(root_id,gname)
      oname = out_name(fname,gname) 
      ofile_name = '/data/user/mamday/newSQuIDS/nuSQuIDS/resources/python/bindings/ZenWeights/'+sys.argv[2]+gname+'.hd5'
      try:
        outfile = h5py.h5f.create(ofile_name,h5py.h5f.ACC_EXCL)
      except:
        outfile = h5py.h5f.open(ofile_name,h5py.h5f.ACC_RDWR)
      h5py.h5o.copy(in_file,gname,outfile,oname)
      del outfile
    else:
      continue
  del in_file
