#!/usr/bin/env python
from os.path import expandvars
import math,sys

import icecube
from icecube import genie_icetray, icetray, dataclasses, dataio, phys_services
from icecube.icetray import I3Tray
from I3Tray import *

load("libsim-services")

tray = I3Tray()
#geofile = sys.argv[1]
#infile = sys.argv[2]

#Global Variables. Ungh
ncCount_ = 0
totCount_ = 0

gcdfile = sys.argv[1]
outfile = sys.argv[2]
#flux = neutrinoflux.ConventionalNeutrinoFlux("honda2006_numu")

#Dumb algorithm to count NC and total events
def genieTest(frame):
  global totCount_,ncCount_
  print 'Sad Failure'
  mcTree = frame['I3MCTree']
  if(frame.Has('I3MCTree')):
    print 'The Stuff'
  primPart = mcTree.most_energetic_primary
  type = primPart.type
  print type
  if(type==icecube.dataclasses.I3Particle.ParticleType.NuMu or type==icecube.dataclasses.I3Particle.ParticleType.NuMuBar):
    energy = primPart.energy
    costheta = math.cos(primPart.dir.zenith)
#    atmoflux = flux.getFlux(type, energy, costheta)
    atmoflux = 1
    pdgCode = primPart.pdg_encoding
    weightInfo = frame['I3MCWeightDict']
    oneWeight = weightInfo['OneWeight']
    intType = weightInfo['InteractionType']
    #print intType,type, energy, costheta
    if(energy>0):
      totCount_+=(atmoflux*oneWeight)
      if(intType==2):
        ncCount_+=(atmoflux*oneWeight)


#tray.AddModule('I3Reader', 'reader',
#               FilenameList = [geofile, infile]
#               )

#tray.AddModule('Delete','deleteMCTree',
#                Keys=['I3MCTree','I3MCWeightDict'])

# if we're dealing with Q frames, set up the header
tray.AddModule("I3InfiniteSource","streams",
               Stream=icetray.I3Frame.DAQ,
               prefix=gcdfile
               )

tray.AddModule("I3MCEventHeaderGenerator","gen_header",
               Year=2009,
               DAQTime=158100000000000000,
               RunNumber=1,
               EventID=1,
               IncrementEventID=True)

genSeed = 1001 

# Now fire up the random number generator with that seed
randomService = phys_services.I3SPRNGRandomService(
    seed = genSeed,
    nstreams = 10000,
    streamnum = 99)


# Lots of parameters get set here, so pay attention!
tray.AddModule("I3GENIEGenerator","genie_generator",
    RandomService = randomService, # alternatively, this can be None and the I3RandomService can be installed using tray.AddService()
    SplineFilename = expandvars("$I3_SRC/genie-icetray/resources/splines/splines_water_2.6.4.xml"),
    LHAPDFPath = expandvars("$I3_SRC/genie-icetray/resources/PDFsets"),
    NuEnergyMin = 3.*I3Units.GeV,
    NuEnergyMax = 100.*I3Units.GeV,
    PowerLawIndex = 2., # E^0 spectrum
    GenVolRadius = 800.*I3Units.m,
    GenVolLength = 1200.*I3Units.m,
    GenVolDepth = 1950.*I3Units.m,
    NeutrinoFlavor = "NuMu", # generates neutrinos and anti-neutrinos (1:1)
    MaterialDensity = 0.93*I3Units.g/I3Units.cm3, # ice density
    TargetMixIngredients = [1000080160,1000010010], # O16, H1
    TargetMixQuantities = [1,2], # H2O (O16->1x, H1->2x)
    ForceSingleProbScale = True,
    NEvents = 100000)

# change the results into an MC Tree
tray.AddModule("I3GENIEResultDictToMCTree", "toMcTree")
tray.AddModule('I3GeometryDecomposer', 'decompose', DeleteI3Geometry=False)

#tray.AddModule(genieTest, 'gTest')

tray.AddModule('I3Writer', 'writer',
    Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics],
#    filename='/net/user/mamday/icesim/scripts/output/PinguSim/'+outfile)
    filename=outfile)

tray.AddModule('TrashCan', 'trash')
tray.Execute()
tray.Finish()

#print 'NC Fraction: ',float(ncCount_)/float(totCount_)
