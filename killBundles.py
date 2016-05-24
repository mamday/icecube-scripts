#!/usr/bin/env python

import icecube
from icecube import icetray, dataio, dataclasses, TopologicalSplitter,santa

from CorridorCut import CorridorCut
from icecube.icetray import *
from I3Tray import * 

import sys,os

tray = I3Tray()

geofile = sys.argv[1]
infile = sys.argv[2]

tray.Add('I3Reader', FilenameList = [geofile, infile])

tray.AddModule('ttrigger<I3RecoPulse>', 'OP_ttrigger',
               Topo                    =    1,
               InputNames              =    ['MaskedOfflinePulses'],   # Pass it *all* the multi pulses 
               OutputName              =    'OTT',
               XYDist                  =    150*I3Units.m,         # max distance in x-y plane
               ZDomDist                =    15,                    # max DOM spacing on a string
               TimeCone                =    450*I3Units.ns,        # max deviation from muon crossing time
               Multiplicity            =    5,                     # min number of pulses for a topo trigger
               )

tray.AddModule('ttrigger<I3RecoPulse>', 'SRT_ttrigger',
               Topo                    =    1,
               InputNames              =    ['TWSRTOfflinePulses'],   # Pass it *all* the multi pulses 
               OutputName              =    'SRTTT',
               XYDist                  =    150*I3Units.m,         # max distance in x-y plane
               ZDomDist                =    15,                    # max DOM spacing on a string
               TimeCone                =    450*I3Units.ns,        # max deviation from muon crossing time
               Multiplicity            =    5,                     # min number of pulses for a topo trigger
               )

tray.AddSegment(santa.SANTA_segment, 'SANTA_standard',
                InputPulseSeries  = 'OfflinePulses',
                OutputPulseSeries = 'SANTA_DirectPulses',
                LoopLevels        = 5.,
                AmplitudeCut_HS   = 1.,
                TimeDelay         = 20. * icetray.I3Units.ns,
                DC_only           = False,
                LFname            = 'LineFit_SANTA',
                FitResultsZenith  = 'SANTA_FitResultsZenith',
                FitResultsCascade = 'SANTA_FitResultsCascade',
                Interactive       = False,
                Debugging         = False,
                santa_suffix      = '',     # Use if the fit is done more than once,
                StrongFitQuality  = False,
                )

tray.AddModule(CorridorCut, 'MyCorridor',
               InputPulseSeries = 'OfflinePulses',
               SANTAFit         = 'SANTA_FitResultsZenith',
               )

tray.Add('I3Writer',filename='/data/ana/LE/Background/Bundles/'+sys.argv[3])

tray.Execute()
tray.Finish()

