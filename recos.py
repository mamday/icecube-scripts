#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################
#
# Collection of reconstructions
# 
# gulliver_commons, CredoFit and MonopodFit adapted from
# Level 3 processing by Jakob van Santen
#
# Edited by Marcel Usner
#
################################################################

from icecube.icetray import load
from icecube.icetray import I3Units, traysegment

def gulliver_commons(tray, params, photonics=True, photosplines=True):
	"""
	Common infrastructure needed for all Gulliver reconstructions:
	Random number services and photonics.
	"""
	load("libphotonics-service", False)
	load("libphys-services", False)

	if photonics:
		tray.AddService('I3GSLRandomServiceFactory', 'I3RandomService')
		tray.AddService('I3PhotonicsServiceFactory','cscd_table_photonics',
		    PhotonicsTopLevelDirectory=params.PhotonicsTabledirCscd,
	    	DriverFileDirectory=params.PhotonicsDriverdirCscd,
		    PhotonicsLevel2DriverFile=params.PhotonicsDriverfileCscd,
		    PhotonicsTableSelection=2, ServiceName='CascadeTablePhotonicsService')
	
	if photosplines:
		tray.AddService('I3PhotoSplineServiceFactory','cscd_spline_photonics',
		    AmplitudeTable=params.PhotoSplineAmplitudeTableCscd,
	    	TimingTable=params.PhotoSplineTimingTableCscd,
		    TimingSigma=0.0, # No convolution for now.
		    ServiceName='CascadeSplinePhotonicsService')
		tray.AddService('I3PhotoSplineServiceFactory','muon_spline_photonics',
		    AmplitudeTable=params.PhotoSplineAmplitudeTableMuon,
		    TimingTable=params.PhotoSplineTimingTableMuon,
	    	TimingSigma=0.0, # No convolution for now.
		    ServiceName='MuonSplinePhotonicsService')

