#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################
#
# Igelfit script for PINGU dataset
#
# Author: Marcel Usner
#
################################################################

################################################################
########################## IMPORTS #############################
################################################################

# IceCube imports
from icecube import icetray, WaveCalibrator, wavedeform, dataio, dataclasses,phys_services
from I3Tray import *
from icecube import santa, millipede, clast

# Python system imports
import os, sys, datetime, time, glob, math, operator
from optparse import OptionParser

# Custom imports
from icecube.millipede import MonopodFit
from recos import gulliver_commons



################################################################
########################### PARSER #############################
################################################################

# Define parser
parser = OptionParser()
usage = """%prog [options] output.i3 input1.i3 [input2.i3] ..."""
parser.set_usage(usage)
parser.add_option("-g", "--gcd", action="store", type="string", default="", dest="GCD", help="Input GCD i3 file")

# Get parsed args
(options,args) = parser.parse_args()
GCD = options.GCD
outputfile = args[0]
inputfiles = args[1]
#if GCD:
#	filenamelist = [GCD] + inputfiles
#else:

gcdfile = dataio.I3File(options.GCD)

geo_frame = gcdfile.pop_frame()
while not geo_frame.Has('I3Geometry'): geo_frame = gcdfile.pop_frame()
geometry_ = geo_frame.Get('I3Geometry')

filenamelist = inputfiles
if len(args) < 2:
	print 'Usage: %prog [options] output.i3 input1.i3 [input2.i3] ...'
	sys.exit(1)

################################################################
################# CONSTANTS / FIELDS ###########################
################################################################

# event counter
total_events = 0		# number of total events
saved_events = 0		# number of saved events

#Mask DOMs
ic86 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,84,86]
#ic86 = [ 17,18,19,25,26,27,28,34,35,36,37,38,44, 45,46,47,54,55,56,79,80,81,82,83,84,85,86]
#ic86 =[ 26,27,35,36,37, 45,46,79,80,81,82,83,84,85,86]
################################################################
########################## METHODS #############################
################################################################

def enum(**enums):
    return type('Enum', (), enums)

#def tracker(frame, flag):

#	global total_events, saved_events

#	if flag == 'first':
#		total_events += 1
#	elif flag == 'last':
#		saved_events += 1

#Pulse Series
uncleaned_pulses = 'OfflinePulses'
#cleaned_pulses = 'SRT_TW_Cleaned_'+uncleaned_pulses
cleaned_pulses = uncleaned_pulses+'_sRT'
ic86_uncleaned_pulses = 'IC86_SDC_'+uncleaned_pulses
ic86_cleaned_pulses = 'IC86_SDC_'+cleaned_pulses

def GetCore(frame):
  if(frame.Has("OfflinePulses_sRT")):
    srtMask = frame["OfflinePulses_sRT"]
    srtPulse = srtMask.apply(frame)
    if(len(srtPulse)>0):
      pulseList = []
      firstStrings = []
#Store srtPulse information in a  list of tuples with time variable first
      for omKey, series in srtPulse:
        if(len(series)>0):
          pulseTup = series[0].time, omKey.string, omKey, geometry_.omgeo[omKey].position[2]
          pulseList.append(pulseTup)
#Get number of hits on each string
      stringList = [i[1] for i in sorted(pulseList)]
      stringCount = [stringList.count(j) for j in stringList]
#Make pulseList sorted in Time
      pulseList.sort()
      if(len([i for i in stringCount if i>2])>0):
        frame["ThreePosX"] = dataclasses.I3Double(geometry_.omgeo[[i for i,j in srtPulse][stringCount.index(min([i for i in stringCount if i>2]))]].position[0])
        frame["ThreePosY"] = dataclasses.I3Double(geometry_.omgeo[[i for i,j in srtPulse][stringCount.index(min([i for i in stringCount if i>2]))]].position[1])
        frame["ThreePosZ"] = dataclasses.I3Double(geometry_.omgeo[[i for i,j in srtPulse][stringCount.index(min([i for i in stringCount if i>2]))]].position[2])
      else:
        return False

def make_seed(frame):
  fPart = frame["CascadeLast_DC"]
  myPart = dataclasses.I3Particle(fPart)
  myPartP3X = dataclasses.I3Particle(fPart)
  myPartP3Y = dataclasses.I3Particle(fPart)
  myPartP3Z = dataclasses.I3Particle(fPart)
  myPartN3X = dataclasses.I3Particle(fPart)
  myPartN3Y = dataclasses.I3Particle(fPart)
  myPartN3Z = dataclasses.I3Particle(fPart)
  xPos = frame["ThreePosX"].value
  yPos = frame["ThreePosY"].value
  zPos = frame["ThreePosZ"].value
  myPart.pos = dataclasses.I3Position(xPos,yPos,zPos)
  myPartP3X.pos = dataclasses.I3Position(xPos+3,yPos,zPos)
  myPartP3Y.pos = dataclasses.I3Position(xPos,yPos+3,zPos)
  myPartP3Z.pos = dataclasses.I3Position(xPos,yPos,zPos+3)
  myPartN3X.pos = dataclasses.I3Position(xPos-3,yPos,zPos)
  myPartN3Y.pos = dataclasses.I3Position(xPos,yPos-3,zPos)
  myPartN3Z.pos = dataclasses.I3Position(xPos,yPos,zPos-3)
  frame["MySeed"] = myPart
  frame["MySeedP3X"] = myPartP3X
  frame["MySeedP3Y"] = myPartP3Y
  frame["MySeedP3Z"] = myPartP3Z
  frame["MySeedN3X"] = myPartN3X
  frame["MySeedN3Y"] = myPartN3Y
  frame["MySeedN3Z"] = myPartN3Z


def monopod_based_cuts(frame):
    CutsPassed=icetray.I3Bool()
    CutsPassed.value=True

    mono=frame["TimedMonopodFit12"]
    #print mono.pos.z, mono.energy, math.sqrt((mono.pos.x-46)**2+(mono.pos.y+34)**2)
    if mono.pos.z>-180:
        CutsPassed.value=False
    if math.sqrt((mono.pos.x-46)**2+(mono.pos.y+34)**2)>150:
        CutsPassed.value=False
    if mono.energy > 200:
        CutsPassed.value=False
    frame["NewBgRejCuts"]=CutsPassed
    if(CutsPassed.value==True):
      return True
    else:
      return False


def selector(omkey,index,pulse):
    truthBool = False
    for i in xrange(len(ic86)):
      if(omkey.string==ic86[i]):
        truthBool = True 
        break 
      else: 
        truthBool = False	
    if(truthBool):
      return truthBool

def MaskPulses(frame):
  frame[ic86_cleaned_pulses]= dataclasses.I3RecoPulseSeriesMapMask(frame, cleaned_pulses, selector)
  frame[ic86_uncleaned_pulses]= dataclasses.I3RecoPulseSeriesMapMask(frame, uncleaned_pulses, selector)
#  utestpulse = dataclasses.I3RecoPulseSeriesMapMask(frame, uncleaned_pulses, selector)
#  uIter = utestpulse.apply(frame)
#  ctestpulse = dataclasses.I3RecoPulseSeriesMapMask(frame, cleaned_pulses, selector)
#  cIter = ctestpulse.apply(frame)
#  print 'Here',len(uIter),len(cIter)
  if(not(ic86_cleaned_pulses) or not(ic86_uncleaned_pulses)):
    return False
#  utestpulse = dataclasses.I3RecoPulseSeriesMapMask(frame, uncleaned_pulses, selector)
#  uIter = utestpulse.apply(frame)
#  for omkey,pulse in uIter:
#    print omkey.string

#  frame[ic86_uncleaned_pulses]= uIter 
  
#print ""
#print "Starting I3Tray..."
#starttime = datetime.datetime.now()

tray = I3Tray()


tray.AddModule('I3Reader', 'reader', FilenameList=[GCD, inputfiles])

tray.AddModule(GetCore,"Corer")

tray.AddModule(make_seed,"Seeder")

#Alexander's Fix
tray.AddModule('I3WaveformTimeRangeCalculator','WaveformTimeRangeCalculator',
#If            = lambda frame: TestForMissingTimeRange,
WaveformRange = 'WaveformTimeRange' )

#tray.AddModule(MaskPulses,'theMask')

tray.AddModule(wavedeform.AddMissingTimeWindow,'AddMissingTimeWindow',
Pulses = 'OfflinePulses', 
WaveformTimeRange = 'WaveformTimeRange')

tray.AddModule(wavedeform.AddMissingTimeWindow,'AddMissingTimeWindow_sRT',
Pulses = 'OfflinePulses_sRT', 
WaveformTimeRange = 'WaveformTimeRange')

#tray.AddModule(tracker, 'tracker_first', flag='first')


#Variables
clast_id                = 'ClastRefit'               # name of clast vertex seed
mono_id                 = 'TimedMonopodFit12'   # name of the timed monopod fit
primary_id              = 'PrimaryNu'           # name of primary particle
photons_per_bin = 1


#Photonics
topleveldir = '/net/user/mntobin/IceRec/Tables/'
spline_tables = enum(
#               PhotoSplineAmplitudeTableCscd   = topleveldir + '/ems_spice1_z20_a10.abs.fits',
#               PhotoSplineTimingTableCscd      = topleveldir + '/ems_spice1_z20_a10.prob.fits',
  PhotoSplineAmplitudeTableCscd   = topleveldir + '/ems_mie_z20_a10_150.abs.fits',
  PhotoSplineTimingTableCscd      = topleveldir + '/ems_mie_z20_a10_150.prob.fits',
#               PhotoSplineAmplitudeTableMuon   = topleveldir + '/emu_abs.fits',
#               PhotoSplineTimingTableMuon      = topleveldir + '/emu_prob.fits')
  PhotoSplineAmplitudeTableMuon   = topleveldir + '/emu_abs150.fits',
  PhotoSplineTimingTableMuon      = topleveldir + '/emu_prob150.fits')

gulliver_commons(tray, spline_tables, photonics=False)

#Seed
#tray.AddModule('I3CLastModule', 'clast',
#        InputReadout=   cleaned_pulses,#Clean
#        Name=           clast_id,
#        EnergyParam0=   -3.3,
#        EnergyParam1=   9.2,
#        EnergyParam2=   -9.7,
#        EnergyParam3=   5.3,
#        EnergyParam4=   -1.4,
#        EnergyParam5=   0.134)

#tray.AddModule('I3CLastModule', 'clast',
#        InputReadout=   'OfflinePulses_sRT',#Clean
#        Name=           clast_id,
#        EnergyParam0=   -3.3,
#        EnergyParam1=   9.2,
#        EnergyParam2=   -9.7,
#        EnergyParam3=   5.3,
#        EnergyParam4=   -1.4,
#        EnergyParam5=   0.134)

#tray.AddModule('I3CLastModule', 'clast_S6',
#        InputReadout=   'String6Pulses',#Clean
#        Name=           clast_id+'_S6',
#        EnergyParam0=   -3.3,
#        EnergyParam1=   9.2,
#        EnergyParam2=   -9.7,
#        EnergyParam3=   5.3,
#        EnergyParam4=   -1.4,
#        EnergyParam5=   0.134)


# Include Monopod ########################################################
tray.AddSegment(MonopodFit, mono_id,
        Photonics=              'CascadeSplinePhotonicsService',
        Iterations=             12,
        Pulses=                 'OfflinePulses',
        Seed=                   'MySeed',
        PhotonsPerBin=          photons_per_bin,
        )
tray.AddSegment(MonopodFit, mono_id+'_P3X',
        Photonics=              'CascadeSplinePhotonicsService',
        Iterations=             12,
        Pulses=                 'OfflinePulses',
        Seed=                   'MySeedP3X',
        PhotonsPerBin=          photons_per_bin,
        )
tray.AddSegment(MonopodFit, mono_id+'_P3Y',
        Photonics=              'CascadeSplinePhotonicsService',
        Iterations=             12,
        Pulses=                 'OfflinePulses',
        Seed=                   'MySeedP3Y',
        PhotonsPerBin=          photons_per_bin,
        )
tray.AddSegment(MonopodFit, mono_id+'_P3Z',
        Photonics=              'CascadeSplinePhotonicsService',
        Iterations=             12,
        Pulses=                 'OfflinePulses',
        Seed=                   'MySeedP3Z',
        PhotonsPerBin=          photons_per_bin,
        )
tray.AddSegment(MonopodFit, mono_id+'_N3X',
        Photonics=              'CascadeSplinePhotonicsService',
        Iterations=             12,
        Pulses=                 'OfflinePulses',
        Seed=                   'MySeedN3X',
        PhotonsPerBin=          photons_per_bin,
        )
tray.AddSegment(MonopodFit, mono_id+'_N3Y',
        Photonics=              'CascadeSplinePhotonicsService',
        Iterations=             12,
        Pulses=                 'OfflinePulses',
        Seed=                   'MySeedN3Y',
        PhotonsPerBin=          photons_per_bin,
        )
tray.AddSegment(MonopodFit, mono_id+'_N3Z',
        Photonics=              'CascadeSplinePhotonicsService',
        Iterations=             12,
        Pulses=                 'OfflinePulses',
        Seed=                   'MySeedN3Z',
        PhotonsPerBin=          photons_per_bin,
        )

tray.AddSegment(MonopodFit, mono_id+'_sRT',
        Photonics=              'CascadeSplinePhotonicsService',
        Iterations=             12,
        Pulses=                 'OfflinePulses_sRT',
        Seed=                   'CascadeLast_DC',
        PhotonsPerBin=          photons_per_bin,
        )


#tray.AddSegment(MonopodFit, mono_id+'_CS3',
#        Photonics=              'CascadeSplinePhotonicsService',
#        Iterations=             12,
#        Pulses=                 'String3Pulses',
#        Seed=                   clast_id+'_S3',
#        PhotonsPerBin=          photons_per_bin,
#        )
#tray.AddSegment(MonopodFit, mono_id+'_S6',
#        Photonics=              'CascadeSplinePhotonicsService',
#        Iterations=             12,
#        Pulses=                 'String6Pulses',
#        Seed=                   clast_id,
#        PhotonsPerBin=          photons_per_bin,
#        )
#tray.AddSegment(MonopodFit, mono_id+'_CS6',
#        Photonics=              'CascadeSplinePhotonicsService',
#        Iterations=             12,
#        Pulses=                 'String6Pulses',
#        Seed=                   clast_id+'_S6',
#        PhotonsPerBin=          photons_per_bin,
#        )

#tray.AddModule(monopod_based_cuts,'MCuts')

# Finish the tray ################################################################

#tray.AddModule(tracker, 'tracker_last', flag='last')

tray.AddModule('I3Writer', 'writer', 
Filename='/net/user/mamday/icesim/scripts/output/Mono/'+outputfile, 
#Filename=outputfile, 
DropOrphanStreams=[icetray.I3Frame.DAQ], 
Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics])
tray.AddModule('TrashCan','can')
tray.Execute()
tray.Finish()

#print "Finished I3Tray! This took: ", datetime.datetime.now() - starttime
#print "Number of events (saved / total): %i / %i" % (saved_events, total_events)
#print ""

