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
from icecube import icetray, improvedLinefit, gulliver_modules, lilliput, gulliver, WaveCalibrator, wavedeform, dataio, dataclasses, phys_services
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

def tracker(frame, flag):

	global total_events, saved_events

	if flag == 'first':
		total_events += 1
	elif flag == 'last':
		saved_events += 1

#Pulse Series
uncleaned_pulses = 'OfflinePulses'
#cleaned_pulses = 'SRT_TW_Cleaned_'+uncleaned_pulses
cleaned_pulses = uncleaned_pulses+'_sRT'
ic86_uncleaned_pulses = 'IC86_SDC_'+uncleaned_pulses
ic86_cleaned_pulses = 'IC86_SDC_'+cleaned_pulses

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
  
print ""
print "Starting I3Tray..."
#starttime = datetime.datetime.now()

tray = I3Tray()

tray.AddModule('I3Reader', 'reader', FilenameList=[GCD, inputfiles])

####tray.AddModule("I3NullSplitter", "mysplit", InputPulseSeries = 'WavedeformPulses')

def selEvent(frame):
  evt_id = frame["I3EventHeader"].event_id
  print 'Event: ',evt_id
  if(evt_id!=6802):
    return False

#tray.AddModule(selEvent,'select')

#Alexander's Fix
tray.AddModule('I3WaveformTimeRangeCalculator','WaveformTimeRangeCalculator',
#If            = lambda frame: TestForMissingTimeRange,
WaveformRange = 'WaveformTimeRange' )

#tray.AddModule(MaskPulses,'theMask')

#Improved Pulses
'''
tray.AddModule('DelayCleaning', 'DelayCleaning_imp',
               InputResponse  = uncleaned_pulses,
               OutputResponse = 'imp_delayCleaned'
               )
tray.AddModule('HuberFit', 'HuberFit_imp',
               Name            = 'HuberFit_imp',
               InputRecoPulses = 'imp_delayCleaned'
               )
tray.AddModule('Debiasing', 'Debiasing_imp',
               InputResponse  = 'imp_delayCleaned',
               OutputResponse = 'imp_debiased',
               Seed           = 'HuberFit_imp'
               )
'''

tray.AddModule(wavedeform.AddMissingTimeWindow,'AddMissingTimeWindow',
Pulses = uncleaned_pulses, 
WaveformTimeRange = 'WaveformTimeRange')

tray.AddModule(tracker, 'tracker_first', flag='first')


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

tray.AddModule('I3CLastModule', 'clast',
        InputReadout=   uncleaned_pulses,#Clean
        Name=           clast_id,
        EnergyParam0=   -3.3,
        EnergyParam1=   9.2,
        EnergyParam2=   -9.7,
        EnergyParam3=   5.3,
        EnergyParam4=   -1.4,
        EnergyParam5=   0.134)

def addPrimMu(frame):
  #mostEnergetic = frame["I3MCTree"].most_energetic_primary
  mostEnergetic = frame[clast_id]
  #mostEnergetic.shape = dataclasses.I3Particle.ParticleShape.ContainedTrack
  #mostEnergetic.fit_status = mostEnergetic.OK
  frame['MyMuon'] = mostEnergetic

tray.AddModule(addPrimMu,'addMu')


# Include Monopod ########################################################
'''tray.AddSegment(MonopodFit, mono_id,
        Photonics=              'CascadeSplinePhotonicsService',
        Iterations=             12,
        Pulses=                 uncleaned_pulses,
        Seed=                   'MyMuon',
        PhotonsPerBin=          photons_per_bin,
        )
'''

#tray.AddService("I3GulliverLBFGSBFactory", 'minuit',
#  MaxIterations=1000,
#  Tolerance=1e-3,
#  GradientTolerance=1,
#)

'''
tray.AddService('I3GulliverMinuit2Factory', 'minuit',
    MaxIterations=2000, Tolerance=0.1, Algorithm='SIMPLEX')

tray.AddService('I3BasicSeedServiceFactory', 'seed', FirstGuess='SPEFit2_DC',
    TimeShiftType='TNone')

tray.AddService('I3SimpleParametrizationFactory','simplesmall',
                StepX       = 5*I3Units.m,
                StepY       = 5*I3Units.m,
                StepZ       = 5*I3Units.m,
                StepZenith  = 0.05*I3Units.radian,
                StepAzimuth = 0.2*I3Units.radian,
                BoundsX     = [-200*I3Units.m,200*I3Units.m],
                BoundsY     = [-200*I3Units.m,200*I3Units.m],
                BoundsZ     = [-500*I3Units.m,-200*I3Units.m]
                )
'''
#tray.AddService('I3GulliverIPDFPandelFactory', 'SPEPandel_Muon_S3',
#                InputReadout      =  'String3Pulses',                  # ! Use debiased pulses
#                Likelihood        =  'SPEAll' ,                       # Default
#                PEProb            =  'GaussConvoluted' ,              # Default (New version of gauss convoluted!)
#                AbsorptionLength  =  98.0 * I3Units.m ,               # Default
#                JitterTime        =  15 * I3Units.ns ,                # Default
#                NoiseProbability  =  1e-9 * I3Units.hertz ,
#                EventType         =  'InfiniteMuon' ,                 # Default
#                IceModel          =  2 ,                              # Default
#                IceFile           =  ''                               # Default
#                )

#tray.AddService('I3GulliverIPDFPandelFactory', 'SPEPandel_Casc_S3',
#                InputReadout      =  'String3Pulses',                  # ! Use debiased pulses
#                Likelihood        =  'SPEAll' ,                       # Default
#                PEProb            =  'GaussConvoluted' ,              # Default (New version of gauss convoluted!)
#                AbsorptionLength  =  98.0 * I3Units.m ,               # Default
#                JitterTime        =  15 * I3Units.ns ,                # Default
#                NoiseProbability  =  1e-9 * I3Units.hertz ,
#                EventType         =  'DirectionalCascade' ,                 # Default
##                EventType         =  'InfiniteMuon' ,                 # Default
#                IceModel          =  2 ,                              # Default
#                IceFile           =  ''                               # Default
#                )

#tray.AddService('I3GulliverIPDFPandelFactory', 'SPEPandel_Muon_OP',
#                InputReadout      =  'OfflinePulses_sRT',                  # ! Use debiased pulses
#                Likelihood        =  'SPEAll' ,                       # Default
#                PEProb            =  'GaussConvoluted' ,              # Default (New version of gauss convoluted!)
#                AbsorptionLength  =  98.0 * I3Units.m ,               # Default
#                JitterTime        =  15 * I3Units.ns ,                # Default
#                NoiseProbability  =  10 * I3Units.hertz ,
#                EventType         =  'InfiniteMuon' ,                 # Default
#                IceModel          =  2 ,                              # Default
#                IceFile           =  ''                               # Default
#                )

#tray.AddService('I3GulliverIPDFPandelFactory', 'SPEPandel_Casc_OP',
#                InputReadout      =  'OfflinePulses_sRT',                  # ! Use debiased pulses
#                Likelihood        =  'SPEAll' ,                       # Default
#                PEProb            =  'GaussConvoluted' ,              # Default (New version of gauss convoluted!)
#                AbsorptionLength  =  98.0 * I3Units.m ,               # Default
#                JitterTime        =  15 * I3Units.ns ,                # Default
#                NoiseProbability  =  10 * I3Units.hertz ,
#                EventType         =  'DirectionalCascade' ,                 # Default
#                IceModel          =  2 ,                              # Default
#                IceFile           =  ''                               # Default
#                )


#tray.AddService('I3GulliverIPDFPandelFactory', 'SPEPandel_Muon_S6',
#                InputReadout      =  'String6Pulses',                  # ! Use debiased pulses
#                Likelihood        =  'SPEAll' ,                       # Default
#                PEProb            =  'GaussConvoluted' ,              # Default (New version of gauss convoluted!)
#                AbsorptionLength  =  98.0 * I3Units.m ,               # Default
#                JitterTime        =  15 * I3Units.ns ,                # Default
#                NoiseProbability  =  1e-9 * I3Units.hertz ,
#                EventType         =  'InfiniteMuon' ,                 # Default
#                IceModel          =  2 ,                              # Default
#                IceFile           =  ''                               # Default
#                )

#tray.AddService('I3GulliverIPDFPandelFactory', 'SPEPandel_Casc_S6',
#                InputReadout      =  'String6Pulses',                  # ! Use debiased pulses
#                Likelihood        =  'SPEAll' ,                       # Default
#                PEProb            =  'GaussConvoluted' ,              # Default (New version of gauss convoluted!)
#                AbsorptionLength  =  98.0 * I3Units.m ,               # Default
#                JitterTime        =  15 * I3Units.ns ,                # Default
#                NoiseProbability  =  1e-9 * I3Units.hertz ,
#                EventType         =  'DirectionalCascade' ,                 # Default
#                EventType         =  'InfiniteMuon' ,                 # Default
#                IceModel          =  2 ,                              # Default
#                IceFile           =  ''                               # Default
#                )

#tray.AddModule('I3IterativeFitter', 'SPEFit6_Muon_S3',
#               RandomService    =  'SOBOL',                  # ! Name of randomizer service
#               NIterations      =  6,
#               SeedService      =  'seed',      # ! Name of seed service
#               Parametrization  =  'simplesmall',            # ! Name of track parametrization service
#               LogLikelihood    =  'SPEPandel_Muon_S3',          # ! Name of likelihood service
#               Minimizer        =  'minuit',                 # ! Name of minimizer service
#)

#tray.AddModule('I3IterativeFitter', 'SPEFit6_Muon_S6',
#               RandomService    =  'SOBOL',                  # ! Name of randomizer service
#               NIterations      =  6,
#               SeedService      =  'seed',      # ! Name of seed service
#               Parametrization  =  'simplesmall',            # ! Name of track parametrization service
#               LogLikelihood    =  'SPEPandel_Muon_S6',          # ! Name of likelihood service
#               Minimizer        =  'minuit',                 # ! Name of minimizer service
#)

#tray.AddModule('I3IterativeFitter', 'SPEFit6_Casc_S3',
#               RandomService    =  'SOBOL',                  # ! Name of randomizer service
#               NIterations      =  6,
#               SeedService      =  'seed',      # ! Name of seed service
#               Parametrization  =  'simplesmall',            # ! Name of track parametrization service
#               LogLikelihood    =  'SPEPandel_Casc_S3',          # ! Name of likelihood service
#               Minimizer        =  'minuit',                 # ! Name of minimizer service
#)

#tray.AddModule('I3IterativeFitter', 'SPEFit6_Casc_S6',
#               RandomService    =  'SOBOL',                  # ! Name of randomizer service
#               NIterations      =  6,
#               SeedService      =  'seed',      # ! Name of seed service
#               Parametrization  =  'simplesmall',            # ! Name of track parametrization service
#               LogLikelihood    =  'SPEPandel_Casc_S6',          # ! Name of likelihood service
#               Minimizer        =  'minuit',                 # ! Name of minimizer service
#)

#tray.AddModule('I3IterativeFitter', 'SPEFit6_Muon_OP',
#               RandomService    =  'SOBOL',                  # ! Name of randomizer service
#               NIterations      =  6,
#               SeedService      =  'seed',      # ! Name of seed service
#               Parametrization  =  'simplesmall',            # ! Name of track parametrization service
#               LogLikelihood    =  'SPEPandel_Muon_OP',          # ! Name of likelihood service
#               Minimizer        =  'minuit',                 # ! Name of minimizer service
#)
#tray.AddModule('I3IterativeFitter', 'SPEFit6_Casc_OP',
#               RandomService    =  'SOBOL',                  # ! Name of randomizer service
#               NIterations      =  6,
#               SeedService      =  'seed',      # ! Name of seed service
#               Parametrization  =  'simplesmall',            # ! Name of track parametrization service
#               LogLikelihood    =  'SPEPandel_Casc_OP',          # ! Name of likelihood service
#               Minimizer        =  'minuit',                 # ! Name of minimizer service
#)


#tray.AddModule(wavedeform.AddMissingTimeWindow,'AddMissingTimeWindow_3',
#Pulses = 'String3Pulses',
#WaveformTimeRange = 'WaveformTimeRange')
#tray.AddModule(wavedeform.AddMissingTimeWindow,'AddMissingTimeWindow_6',
#Pulses = 'String6Pulses',
#WaveformTimeRange = 'WaveformTimeRange')
#tray.AddModule(wavedeform.AddMissingTimeWindow,'AddMissingTimeWindow_sRT',
#Pulses = ic86_cleaned_pulses,
#WaveformTimeRange = 'WaveformTimeRange')
#tray.AddModule(wavedeform.AddMissingTimeWindow,'AddMissingTimeWindow_imp',
#Pulses = 'imp_debiased',
#WaveformTimeRange = 'WaveformTimeRange')


#tray.AddSegment(millipede.MuMillipedeFit, "MuMillipede_S3", CascadePhotonicsService='CascadeSplinePhotonicsService', Seed='SPEFit2_DC', StepZenith=3, StepAzimuth=10, CascadeSpacing=3, Pulses='String3Pulses')

#tray.AddSegment(millipede.MuMillipedeFit, "MuMillipede_S6", CascadePhotonicsService='CascadeSplinePhotonicsService', Seed='SPEFit2_DC', StepZenith=3, StepAzimuth=10, CascadeSpacing=3, Pulses='String6Pulses')

tray.AddSegment(millipede.MuMillipedeFit, "MuMillipede", CascadePhotonicsService='CascadeSplinePhotonicsService', Seed='MyMuon', StepZenith=3, StepAzimuth=10, CascadeSpacing=3, Pulses=uncleaned_pulses)

#tray.AddSegment(millipede.MuMillipedeFit, "MuMillipede_imp", CascadePhotonicsService='CascadeSplinePhotonicsService', Seed='SPEFit2_DC', StepZenith=3, StepAzimuth=10, CascadeSpacing=3, Pulses='imp_debiased')


#tray.AddSegment(millipede.MuMillipedeFit, "MuMillipede_sRT", CascadePhotonicsService='CascadeSplinePhotonicsService', Seed='SPEFit2_DC', StepZenith=3, StepAzimuth=10, CascadeSpacing=3, Pulses=ic86_cleaned_pulses)

# Finish the tray ################################################################

tray.AddModule(tracker, 'tracker_last', flag='last')

tray.AddModule('I3Writer', 'writer', 
Filename=outputfile, 
#Filename=outputfile, 
DropOrphanStreams=[icetray.I3Frame.DAQ], 
Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics])
tray.AddModule('TrashCan','can')
tray.Execute(8)
tray.Finish()

#print "Finished I3Tray! This took: ", datetime.datetime.now() - starttime
#print "Number of events (saved / total): %i / %i" % (saved_events, total_events)
#print ""

