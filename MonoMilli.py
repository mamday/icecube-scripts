#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################
#
# Random code, some stolen from Igelfit?
#
################################################################

################################################################
########################## IMPORTS #############################
################################################################

# IceCube imports
from icecube import icetray, improvedLinefit, gulliver_modules, lilliput, gulliver, WaveCalibrator, wavedeform, dataio, dataclasses, phys_services
from I3Tray import *
from icecube import millipede, clast

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

########################## METHODS #############################
################################################################

def enum(**enums):
    return type('Enum', (), enums)

def tracker(frame, flag):

	global total_events, saved_events

	if flag == 'first':
		total_events += 1
	elif flag == 'last':
		saved_events += 1

#Pulse Series
uncleaned_pulses = 'WavedeformPulses'
  
print ""
print "Starting I3Tray..."
#starttime = datetime.datetime.now()

tray = I3Tray()

tray.AddModule('I3Reader', 'reader', FilenameList=[GCD, inputfiles])

tray.AddModule("I3NullSplitter", "mysplit", InputPulseSeries = 'WavedeformPulses')

def selEvent(frame):
  evt_id = frame["I3EventHeader"].event_id
  print 'Event: ',evt_id
  if(evt_id!=6802):
    return False 

tray.AddModule(selEvent,'select')

#Alexander's Fix
tray.AddModule('I3WaveformTimeRangeCalculator','WaveformTimeRangeCalculator',
#If            = lambda frame: TestForMissingTimeRange,
WaveformRange = 'WaveformTimeRange' )


mono_id                 = 'MonopodFit12'   # name of the timed monopod fit
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

def addPrimMu(frame):
  mostEnergetic = frame["I3MCTree"].most_energetic_muon
  mostEnergetic.shape = dataclasses.I3Particle.ParticleShape.ContainedTrack
  mostEnergetic.fit_status = mostEnergetic.OK
  frame['MyMuon'] = mostEnergetic

tray.AddModule(addPrimMu,'addMu')


# Include Monopod ########################################################
tray.AddSegment(MonopodFit, mono_id,
        Photonics=              'CascadeSplinePhotonicsService',
        Iterations=             12,
        Pulses=                 uncleaned_pulses,
        Seed=                   'MyMuon',
        PhotonsPerBin=          photons_per_bin,
        )

tray.AddSegment(millipede.MuMillipedeFit, "MuMillipede", CascadePhotonicsService='CascadeSplinePhotonicsService', Seed='MostEnergMuon', StepZenith=3, StepAzimuth=10, CascadeSpacing=3, Pulses='WavedeformPulses')

# Finish the tray ################################################################

tray.AddModule(tracker, 'tracker_last', flag='last')

tray.AddModule('I3Writer', 'writer', 
Filename=outputfile, 
#Filename=outputfile, 
DropOrphanStreams=[icetray.I3Frame.DAQ], 
Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics])

tray.AddModule('TrashCan','can')
tray.Execute()
tray.Finish()

