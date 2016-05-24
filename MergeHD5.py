import h5py
import sys
from glob import glob

outfile = h5py.h5f.create(sys.argv[2],h5py.h5f.ACC_TRUNC)
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
#  print fname
  in_file = h5py.h5f.open(fname, h5py.h5f.ACC_RDONLY)
  root_id = h5py.h5g.open(in_file,"/")

  for gname in root_id:
    group_id = h5py.h5g.open(root_id,gname)
    oname = out_name(fname,gname) 
    h5py.h5o.copy(in_file,gname,outfile,oname)

  del in_file

del outfile
 
