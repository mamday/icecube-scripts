import icecube
from icecube import icetray, dataclasses, phys_services, simclasses, tableio, dataio, hdfwriter, rootwriter
import math
from icecube.icetray import *
from icecube.dataclasses import *
from icecube.phys_services import *

#IC86 Geometry
gcdfile = dataio.I3File('/net/user/mamday/icetray/data/GeometryFiles/GeoCalibDetectorStatus_IC86.55697_corrected_V2.i3')

#PINGU Geometry
gcdfile1 = dataio.I3File('/net/user/mamday/pingusim/GeoCalibDetectorStatus_pingu_V13_Corson_75_s13_d5.i3')

#The new geometry
new_gcdfile = dataio.I3File('Carlyle-40s-13m-60d-5m.i3.gz', dataio.I3File.Mode.Writing)

#IC86 Geometry
geo_frame = gcdfile.pop_frame()
while not geo_frame.Has('I3Geometry'): geo_frame = gcdfile.pop_frame()
geometry = geo_frame.Get('I3Geometry')

#PINGU Geometry
geo_frame1 = gcdfile1.pop_frame()
while not geo_frame1.Has('I3Geometry'): geo_frame1 = gcdfile1.pop_frame()
geometry1 = geo_frame1.Get('I3Geometry')


#IC86 Calibration and Detector Status 
cal_frame = gcdfile.pop_frame()
while not cal_frame.Has('I3Calibration'): cal_frame = gcdfile.pop_frame()
calibration = cal_frame.Get('I3Calibration')

status_frame = gcdfile.pop_frame()
while not status_frame.Has('I3DetectorStatus'): status_frame = gcdfile.pop_frame()
status = status_frame.Get('I3DetectorStatus')

#PINGU Det Status and Calibration
cal_frame1 = gcdfile1.pop_frame()
while not cal_frame1.Has('I3Calibration'): cal_frame1 = gcdfile1.pop_frame()
calibration1 = cal_frame1.Get('I3Calibration')

status_frame1 = gcdfile1.pop_frame()
while not status_frame1.Has('I3DetectorStatus'): status_frame1 = gcdfile1.pop_frame()
status1 = status_frame1.Get('I3DetectorStatus')

#Retrieve DomSets (this is a super lazy method since it gives the full DOMSets of the larger geometry and we only need the geometry in the smaller radius... But I am not going to fix it today)
domsets = status_frame1['DOMSets']

#Set up new GCD objects
newomgeo = dataclasses.I3OMGeo()
newdomcal = dataclasses.I3DOMCalibration()
newdomstat = dataclasses.I3DOMStatus()

#Top and bottom of veto and fiducial regions of IC86
p1 = I3Position(0.,0.,0.)
findkey = icetray.OMKey(86,30,0)
vtopkey = icetray.OMKey(86,1,0)
vbotkey = icetray.OMKey(86,10,0)
ptopkey = icetray.OMKey(86,11,0)
pbotkey = icetray.OMKey(86,60,0)
vtoppos = geometry.omgeo[vtopkey].position
vbotpos = geometry.omgeo[vbotkey].position
ptoppos = geometry.omgeo[ptopkey].position
pbotpos = geometry.omgeo[pbotkey].position

#Information about how I want the geometry to be
nDOMs = 60
nStrings = 75 
radius = 88

#Get the IC86 default
newgeo = geometry
newcal = calibration
newdstat = status

#Paranoia from my C++ days
count = 0

for k in range(1,nStrings):
    for i in range(1,nDOMs+1):
        newkey = OMKey(86+k,i,0)
        newpos = geometry1.omgeo[newkey].position 
        diffx = ptoppos[0]-newpos[0]
        diffy = ptoppos[1]-newpos[1]
        if(math.sqrt(diffx*diffx+ diffy*diffy)<radius):
          #Change the OM key to represent the new geometry
          if(i==1):
              count = count+1
          newnewkey = OMKey(86+count,i,0)

          #Get information from old PINGU geometry
          newomgeo = geometry1.omgeo[newkey]
          newdomcal = calibration1.dom_cal[newkey]
          newdomstat = status1.dom_status[newkey]
          
          #Make new information for the new new key 
          newgeo.omgeo[newnewkey] = newomgeo
          newcal.dom_cal[newnewkey] = newdomcal
          newdstat.dom_status[newnewkey] = newdomstat
          
#Check for existence of created/modified strings
#geo_strings_to_check = range(1,87)
#for s in geo_strings_to_check:
#	found = False
#	for e,p in newgeo.omgeo:
#		print p.position, e
    
#Delete old frame information and make new frames
del geo_frame1['I3Geometry']
geo_frame1['I3Geometry'] = newgeo
del cal_frame1['I3Calibration']
cal_frame1['I3Calibration'] = newcal
del status_frame1['I3DetectorStatus']
status_frame1['I3DetectorStatus'] = newdstat
del status_frame1['DOMSets']
status_frame1['DOMSets'] = domsets

#Save Frame Information
new_gcdfile.push(geo_frame1)
new_gcdfile.push(cal_frame1)
new_gcdfile.push(status_frame1)
new_gcdfile.close()

