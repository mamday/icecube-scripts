#!/usr/bin/env python

import icecube
from icecube import dataclasses,dataio

import sys

infile = dataio.I3File(sys.argv[1])
count = 0
outfile = dataio.I3File('/data/user/mamday/icesim/scripts/output/LNuMu/GenieNuMu_0.i3','w')

while(infile.more()):
  frame = infile.pop_frame()
  count+=1
  outfile.push(frame)
  if(count%100==0):
    outfile.close()
    outfile = dataio.I3File('/data/user/mamday/icesim/scripts/output/LNuMu/GenieNuMu_%i.i3' % (count/100),'w')

  
