import icecube 
from icecube import dataio, icetray, dataclasses, phys_services

import sys

from I3Tray import I3Tray

count = 0
allCount = 0
tray = I3Tray()

tray.Add('I3Reader', FilenameList = sys.argv[1:])

def remFilt(frame):
  global allCount,count
  allCount+=1
  if(frame.Has("FilterMask")):
    if(frame["FilterMask"]["DeepCoreFilter_11"].condition_passed):
      count+=1
      return False
#      return True 
  return False

tray.AddModule(remFilt,'Filter')
tray.Execute()
tray.Finish()

print count,allCount,float(count)/float(allCount)
