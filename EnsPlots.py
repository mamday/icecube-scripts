#!/usr/bin/env python
import cPickle as pickle
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import glob
import sys,numpy,pylab
file_list = glob.glob(sys.argv[1])
llh_dict = {}
for lfile in file_list:
  try:
    llh_file = pickle.load(open(lfile, "rb"))
    mt = float("%.3f" % llh_file['result']['mt'])
    tt = float("%.5f" % llh_file['result']['tt'])
    plt.plot(mt, tt, 'k.', marker='x',markersize=10.0)
    pylab.xlim(-0.015,0.015)
    pylab.ylim(-0.1,0.1)
    pylab.tight_layout()
    pylab.savefig("Ens.pdf")
  except:
    print lfile

