import icecube
from icecube import BadDomList, clsim, wavedeform, vuvuzela, trigger_sim, WaveCalibrator, phys_services, DOMLauncher, icetray, dataclasses, dataio
from I3Tray import I3Tray

from optparse import OptionParser
from os.path import expandvars
import sys
usage = "usage: %prog [options] outputfile"
parser = OptionParser(usage)
parser.add_option("-s", "--seed",type="int",default=12345,
                  dest="SEED", help="Initial seed for the random number generator")
parser.add_option("-g", "--gcd",default="/data/user/mamday/GeoCalibDetectorStatus_pingu_V36_Zezel_40_s22_d3.i3",
                  dest="GCDFILE", help="Read geometry from GCDFILE (.i3{.gz} format)")
parser.add_option("-r", "--runnumber", type="int", default=1,
                  dest="RUNNUMBER", help="The run number for this simulation")
parser.add_option("-n", "--numevents", type="int", default=1000,
                  dest="NUMEVENTS", help="The number of events per run")
parser.add_option("--mode", choices=("hybrid", "table", "gpu"), default="table",
                  dest="MODE", help="How to propagate photons")

# parse cmd line args, bail out if anything is not understood
(options,args) = parser.parse_args()
if len(args) != 3:
	parser.error("You must specify an output file name")
else:
	outfile = sys.argv[1]

tray = I3Tray()

from clsim_server.client_module import GPU_Client

from icecube import MuonGun, sim_services
from icecube.icetray import I3Units
from icecube.dataclasses import *
from icecube.sim_services.propagation import get_propagators
from icecube.MuonGun.segments import GenerateBundles
from icecube.MuonGun import load_model, EnergyDependentSurfaceInjector, ConstantSurfaceScalingFunction, StaticSurfaceInjector, Cylinder, OffsetPowerLaw
# base = expandvars('$I3_SRC/MuonGun/resources/scripts/fitting/')
#Flux model
model = MuonGun.load_model('GaisserH4a_atmod12_SIBYLL')
model.flux.min_multiplicity = 1
model.flux.max_multiplicity = 1
#Inner and outher target surfaces
outSurface = Cylinder(1600*I3Units.m, 800*I3Units.m)
inSurface = Cylinder(500*I3Units.m, 150*I3Units.m, I3Position(46.3,-34.9,-300))
#Sets energy and spectral index of muons
#Jackob's spectrum
#spectrum = MuonGun.OffsetPowerLaw(5.0, 5e2, 200, 1e6)
spectrum = MuonGun.OffsetPowerLaw(5.0, 7e2, int(sys.argv[2]), int(sys.argv[3]))
#spectrum = MuonGun.OffsetPowerLaw(5.2, 7e2, 150, 1e5)
#spectrum = MuonGun.OffsetPowerLaw(2, 1e3, 1e3, 1e5)

#This version only aims at inSurface, but muons originate at outSurface
scaling = MuonGun.ConstantSurfaceScalingFunction(inSurface)
#generator = MuonGun.EnergyDependentSurfaceInjector(outSurface, model.flux, spectrum, model.radius, scaling,0,1)
generator = MuonGun.EnergyDependentSurfaceInjector(outSurface, model.flux, spectrum, model.radius, scaling)
#This version aims at whatever surface you give it, but originates all the muons inside the surface, not at the top layer of ice
#generator = MuonGun.StaticSurfaceInjector(surface, model.flux, spectrum, model.radius)
#Not sure yet what this does?
# generator = MuonGun.Floodlight()

# set up a random number generator
randomService = phys_services.I3SPRNGRandomService(
    seed = options.SEED*2,
    nstreams = 10000,
    streamnum = options.RUNNUMBER)
    
tray.context['I3RandomService'] = randomService

#Generate bundles of muons
tray.AddSegment(GenerateBundles, 'BundleGen', Generator=generator,
    NEvents=options.NUMEVENTS, GCDFile=options.GCDFILE)
print 'GCD',options.GCDFILE
#Propogate the muons in the detector
tray.AddModule('I3PropagatorModule', PropagatorServices=get_propagators(), RandomService=randomService)

tray.AddModule(GPU_Client,'client')

#Make MCPESeries
#tray.AddSegment(clsim.I3CLSimMakeHits, 'goCLSIM',
#                UseCPUs=False,
#                UseGPUs=True,
#                MMCTrackListName = "MMCTrackList",
#                MCPESeriesName="I3MCPESeriesMap",
#                PhotonSeriesName='thePhotons',
#                ParallelEvents=500,
#                OverrideApproximateNumberOfWorkItems = 1024000,
#                RandomService=randomService,
#                IceModelLocation=expandvars("$I3_SRC/clsim/resources/ice/spice_mie"),
#                UnshadowedFraction=1.0,
#                UnWeightedPhotons=True,
#                UseGeant4=False,
#                StopDetectedPhotons=True,
#                DoNotParallelize=True,
#                DOMOversizeFactor=1.,
#                )


# Find out which DOMs are reported as "bad"
#I should also figure out where/how to use this in the new simulation

#from icecube.BadDomList import bad_dom_list_static
#from icecube.BadDomList.bad_dom_list_static import IC86_bad_data_producing_dom_list
#badRun=118768
#txtfile = expandvars('$I3_SRC') + '/BadDomList/resources/scripts/bad_data_producing_doms_list.txt'
#domsToExclude = IC86_bad_data_producing_dom_list(badRun,txtfile)

#Noise
vuvuzela.AddNoise(tray, "vuvuzela")

#Simulate DOM response
tray.AddModule("PMTResponseSimulator","PINGU_rosencrantz",
    Input="I3MCPESeriesMap",
#    Output="weightedI3MCPESeriesMap",
    MergeHits=True,
    )
tray.AddModule("DOMLauncher", "PINGU_guildenstern",
#    Input="weightedI3MCPESeriesMapPulses",
    Output="InIceRawData",
    UseTabulatedPT=True,
    )

#Figure out later if cleaning can still be done...
#tray.AddModule("I3DOMLaunchCleaning","launchcleaningNoise")(
#       ("InIceInput","InIceRawData"),
#       ("InIceOutput","CleanInIceRawData"),
#       ("IceTopInput","IceTopNoiseRawData"),
#       ("IceTopOutput","CleanIceTopNoiseRawData"),
#       ("FirstLaunchCleaning",False) ,
#       ("CleanedKeys",domsToExclude)
#       )

#Only use PINGU trigger for now

tray.AddModule("SimpleMajorityTrigger","PINGUSMT3Noise")(
        ("DataReadoutName","InIceRawData"),
        ("DOMSetsName","DOMSets"),
#        ("TriggerConfigID",1011)
        ("TriggerConfigID",60001)
        )

tray.AddModule("I3GlobalTriggerSim","PINGU_global_trig")

from icecube.trigger_sim.modules.time_shifter import I3TimeShifter

timeshiftargs = { "SkipKeys": ["I3GenieResultDict"]
                   }

tray.AddSegment(trigger_sim.TriggerSim, 'PINGU_triggersim',
    gcd_file=dataio.I3File(options.GCDFILE),   # for trigger auto-configuration
    prune = True,
    time_shift = True,
    time_shift_args = timeshiftargs
)

#Make waveforms
#tray.AddModule('I3WaveCalibrator', 'domcal')

#tray.AddModule('I3Wavedeform', 'deform')

tray.AddModule("Delete","del")(
         ("Keys",['thePhotons']))

#Currently outfile has to be chosen at the command line, might make it an argument?
tray.AddModule('I3Writer', 'writer',
    Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics],
    filename=outfile)

tray.AddModule('TrashCan', 'YesWeCan')
tray.Execute()
tray.Finish()
