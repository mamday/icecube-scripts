from icecube import trigger_sim, WaveCalibrator, DomTools, wavedeform, icepick, phys_services, icetray, dataclasses, dataio
from I3Tray import I3Tray

from glob import glob
from optparse import OptionParser
from os.path import expandvars


# Define parser
parser = OptionParser()
usage = """%prog [options] output.i3 input1.i3 [input2.i3] ..."""
parser.set_usage(usage)
parser.add_option("-g", "--gcd", action="store", type="string", default="", dest="GCD", help="Input GCD i3 file")

# Get parsed args
(options,args) = parser.parse_args()
GCD = options.GCD
outputfile = args[0]
inputfiles = args[1:]

if GCD:
        filenamelist = [GCD] + inputfiles
else:
	filenamelist = inputfiles

if len(args) < 2:
        print 'Usage: %prog [options] output.i3 input1.i3 [input2.i3] ...'
        sys.exit(1)

tray = I3Tray()

tray.AddModule('I3Reader', 'reader', FilenameList=filenamelist)

#Add muon weight that I guess I should have added before
from icecube import MuonGun, sim_services
from icecube.icetray import I3Units
from icecube.dataclasses import *
from icecube.sim_services.propagation import get_propagators
from icecube.MuonGun.segments import GenerateBundles
from icecube.MuonGun import load_model, EnergyDependentSurfaceInjector, ConstantSurfaceScalingFunction, StaticSurfaceInjector, Cylinder, OffsetPowerLaw
#Flux model
model = MuonGun.load_model('GaisserH4a_atmod12_SIBYLL')
model.flux.min_multiplicity = 1
model.flux.max_multiplicity = 1
#Inner and outher target surfaces
outSurface = Cylinder(1600*I3Units.m, 800*I3Units.m)
inSurface = Cylinder(700*I3Units.m, 125*I3Units.m, I3Position(29.3,52.6,-150))
#Sets energy and spectral index of muons
spectrum = MuonGun.OffsetPowerLaw(5.2, 7e2, 200, 1e6)
#This version only aims at inSurface, but muons originate at outSurface
scaling = MuonGun.ConstantSurfaceScalingFunction(inSurface)
generator = MuonGun.EnergyDependentSurfaceInjector(outSurface, model.flux, spectrum, model.radius, scaling,0,1)

tray.AddModule('I3MuonGun::WeightCalculatorModule', 'MuonWeight',
               Model=model, Generator=generator,
               )

tray.AddModule("Delete", "delete_triggerHierarchy",
        Keys=["I3Triggers","I3TriggerHierarchy","TimeShift","WavedeformPulses","WavedeformPulsesTimeRange","CalibratedWaveforms","CalibratedWaveformRange","CalibrationErrata"])


tray.AddModule("SimpleMajorityTrigger","IISMT8")(
               ("DataReadoutName","SelectedInIceRawData"),
               ("TriggerConfigID",1006),
               )

tray.AddModule("ClusterTrigger","string")(
               ("DataReadoutName","SelectedInIceRawData"),
)

tray.AddModule("CylinderTrigger","cyl")(
               ("DataReadoutName","SelectedInIceRawData"),
)

tray.AddModule("SlowMonopoleTrigger","slop")(
               ("DataReadoutName","SelectedInIceRawData"),
)

tray.AddModule("I3GlobalTriggerSim","global_trig",FilterMode=True)

tray.AddModule("I3Pruner","pruner")(
		("DOMLaunchSeriesMapNames",["SelectedInIceRawData","IceTopRawData"]), 
)

from icecube.trigger_sim.modules.time_shifter import I3TimeShifter

time_shift_args = { "I3MCTreeNames": ["I3MCTree"],
                   "I3MCPESeriesMapNames" : ["I3MCPESeriesMap"],
#                   "I3MCHitSeriesMapNames" : ["I3MCHitSeriesMap"],
                   "I3DOMLaunchSeriesMapNames" : ["SelectedInIceRawData","IceTopRawData"]
                   }

parsed_args = dict()

for k,v in time_shift_args.iteritems():
    if k.lower() == "skipkeys" or \
        k.lower() == "referencetriggername":
        parsed_args[k] = v

tray.AddModule(I3TimeShifter,"IC86_MGVuv_shifter",
                       **parsed_args )

#Make waveforms
tray.AddModule('I3WaveCalibrator', 'domcal')(
               ("Launches","SelectedInIceRawData"),

)

tray.AddModule('I3Wavedeform', 'deform')


tray.AddModule('I3Writer', 'writer', 
	Filename='/data/sim/PINGU/2012/triggered/muon_gun/D/'+outputfile, 
	Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics])
tray.AddModule('TrashCan','can')
tray.Execute()
tray.Finish()
