#!/usr/bin/env python

import math,sys

import icecube
from icecube import icetray, neutrinoflux, dataclasses, dataio, phys_services
from icecube.icetray import I3Tray
from I3Tray import *

tray = I3Tray()
geofile = sys.argv[1]
infile = sys.argv[2]

#Global Variables. Ungh
ncCount_ = 0
totCount_ = 0

flux = neutrinoflux.ConventionalNeutrinoFlux("honda2006_nue")

# split Q-frame-only MC files into QP-sequence

#Dumb algorithm to count NC and total events
def countNC(frame):
  global totCount_,ncCount_
  mcTree = frame['I3MCTree']
  primPart = mcTree.most_energetic_primary
  type = primPart.type
  #print type
  if((type==icecube.dataclasses.I3Particle.ParticleType.NuE or type==icecube.dataclasses.I3Particle.ParticleType.NuEBar) and (abs(primPart.pos[0]-29)<30 and abs(primPart.pos[1]-52)<30 and primPart.pos[2]<-150 and primPart.pos[2]>-500)):
    energy = primPart.energy 
    costheta = math.cos(primPart.dir.zenith)
    atmoflux = flux.getFlux(type, energy, costheta)
    pdgCode = primPart.pdg_encoding
    weightInfo = frame['I3MCWeightDict']
    oneWeight = weightInfo['OneWeight']
    intType = weightInfo['InteractionType']
    #print intType,type, energy, costheta
    if(energy>0):
      totCount_+=(atmoflux*oneWeight)
#      totCount_+=1
      if(intType==2):
        ncCount_+=(atmoflux*oneWeight)
#        ncCount_+=1


tray.AddModule('I3Reader', 'reader',
               FilenameList = [geofile, infile]
               )

tray.AddModule("I3NullSplitter", "fullevent", InputPulseSeries = 'WavedeformPulses')

tray.AddModule(countNC, 'leCount')

tray.AddModule('TrashCan', 'trash')
tray.Execute()
tray.Finish()

print float(ncCount_)/float(totCount_)
