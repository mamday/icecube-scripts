import icecube
from icecube import WaveCalibrator,wavedeform,icetray, dataio, dataclasses, millipede
from icecube.icetray import traysegment
from icecube import photonics_service  
import numpy, os, sys, math

from I3Tray import *

#List of keys to remove
delete_keys = []
#Number of minimums to find BlumeFits for
num_mins = 3
#Vertex Seed for the BlumeFit (default is IgelFit)
vert_seed = "Monopod_Clast"
#Tuple of variations. Make square around original seed for now
#BlumeFit zenith and azimuth variations
#pt_tup = [(0,0),(0,10),(10,0),(math.sqrt(200),math.sqrt(200)),(0,-10),(-10,0),(math.sqrt(200),-math.sqrt(200)),(-math.sqrt(200),-math.sqrt(200)),(-math.sqrt(200),math.sqrt(200))]
#Super BlumeFit zenith and azimuth variations
pt_tup = [(0,0),(0,5),(5,0),(0,-5),(-5,0),(0,-20),(-20,0),(0,10),(10,0),(20,0),(0,20),(math.sqrt(800),math.sqrt(800)),(-math.sqrt(800),math.sqrt(800)),(math.sqrt(800),-math.sqrt(800)),(-math.sqrt(800),-math.sqrt(800)),(math.sqrt(50),math.sqrt(50)),(-math.sqrt(50),math.sqrt(50)),(math.sqrt(50),-math.sqrt(50)),(-math.sqrt(50),-math.sqrt(50)),(math.sqrt(200),math.sqrt(200)),(0,-10),(-10,0),(math.sqrt(200),-math.sqrt(200)),(-math.sqrt(200),-math.sqrt(200)),(-math.sqrt(200),math.sqrt(200))]

#Millipede Constants
PhotonsPerBin = 1
Boundary = 800
MuonSpacing = 0 
ShowerSpacing = 2 
Pulses = "newSRT_Cleaned_WavedeformPulses"
BadDOMsList = 'BadDomsList' 

#Useful functions
def makeSeed(vertSeed,zen,azi):
  partPos = vertSeed.pos
  partDir = dataclasses.I3Direction(zen,azi)
  partTime = vertSeed.time
  partLength = vertSeed.length
  partShape = dataclasses.I3Particle.ParticleShape.InfiniteTrack

  seedPart = dataclasses.I3Particle(partPos,partDir,partTime,partShape,partLength)

  return seedPart


#Start tray
tray = I3Tray()
#Run tray and make tray segments
tray.Add("I3Reader",Filenamelist=[sys.argv[1],sys.argv[2]])

topleveldir = '/data/sim/sim-new/ice/photonics-mie-ZeroLengthMuons/'
topleveldir1 = '/data/user/mntobin/IceRec/Tables/'

mabs_table = topleveldir + '/ZeroLengthMieMuons_150_z20_a10.abs.fits' 
cabs_table = topleveldir1 + '/ems_mie_z20_a10_150.abs.fits' 
cprob_table = topleveldir1 + '/ems_mie_z20_a10_150.prob.fits' 
mprob_table = topleveldir + '/ZeroLengthMieMuons_150_z20_a10.prob.fits' 

MuonPhotonicsService = photonics_service.I3PhotoSplineService(mprob_table, mabs_table)
CascadePhotonicsService = photonics_service.I3PhotoSplineService(cprob_table, cabs_table)

tray.AddModule(wavedeform.AddMissingTimeWindow,'AddMissingTimeWindow',
Pulses = Pulses,
WaveformTimeRange = 'WaveformTimeRange')


def Seeder(frame):
  global pt_tup
  print 'Seeding'
  igel_seed = frame[vert_seed]
  zen = igel_seed.dir.zenith
  azi = igel_seed.dir.azimuth
#  for i in xrange(len(pt_tup)):
#    igel_seed = frame[vert_seed]
#    for j in xrange(num_mins):
  #Set values of energy, zenith and azimuth from the current llh minimum
#      energy,zenith,azimuth = GetKinVals(frame,j+1)
#      igel_seed.energy = energy
#      igel_seed.dir = dataclasses.I3Direction(zenith,azimuth)
#      zen = igel_seed.dir.zenith + (numpy.pi/180)*pt_tup[i][0]
#      azi = igel_seed.dir.azimuth + (numpy.pi/180)*pt_tup[i][1]
  #Fix edge cases to keep values between 0 and 2pi. Almost undoubtedly a better way to do this. So, so lazy
#      if(zen>(numpy.pi)): zen = 2*numpy.pi - zen
#      if(zen<0): zen = -1*zen 
#      if(azi>(2*numpy.pi)): azi = azi - (2*numpy.pi)*math.floor(azi/(2*numpy.pi))
#      if(azi<0): azi = azi + (2*numpy.pi)*(1+math.floor(-1*azi/(2*numpy.pi)))
  #Get igelfit seed, modify it, put it in the frame
#      seed_id = 'Seed'+'%i%i' % (i,j)
  seed_id = 'Seed'
  frame[seed_id] = makeSeed(igel_seed,zen,azi)

#Find best fit value (mostly stolen from igelfit)
def BestFit(frame):
  global pt_tup, delete_keys
  print 'Fitting'
  content_map = []
  igel_seed = frame[vert_seed]
  seed_id = 'Seed'
  millipede_id = 'Milli_'
   
  millipede = frame[millipede_id]
  millipede_fitparams = frame[millipede_id + 'FitParams']
  rlogl = millipede_fitparams.rlogl
  content_map.append([rlogl, millipede_id])
  fit = min(content_map, key= lambda content_map : content_map[0]) 
  fit_rlogl = fit[0]
  fit_id = fit[1]
  print 'Looking for the best fit',fit_id
  track_fit = frame[fit_id]
  track_fit_fitparams = frame[fit_id + 'FitParams']

  zenith, azimuth = track_fit[0].dir.zenith, track_fit[0].dir.azimuth
  forged_particle = dataclasses.I3Particle()
  forged_particle.energy = 0
  forged_particle.dir = dataclasses.I3Direction(zenith, azimuth)
  forged_particle.pos.x = igel_seed.pos.x
  forged_particle.pos.y = igel_seed.pos.y
  forged_particle.pos.z = igel_seed.pos.z
  forged_particle.time = igel_seed.time
  forged_particle.speed = 0.299792
  forged_particle.shape = igel_seed.shape.InfiniteTrack

  frame["BlumeFit"]=forged_particle


tray.Add(Seeder)

@traysegment
def Blumefit(tray, name,
             If=lambda frame: True):
      print 'Bluming' 
#Get igelfit seed, modify it, put it in the frame
#      seed_id = 'Seed'+'%i%i' % (i,j)
      seed_id = 'Seed'
#Run MuMillipede for seed particle
      millipede_id = 'Milli_'
      tray.Add("MuMillipede", 'MuBlume',
      	MuonPhotonicsService=           MuonPhotonicsService,
	CascadePhotonicsService=        CascadePhotonicsService,
	PhotonsPerBin=                  PhotonsPerBin,
	MuonSpacing=                    MuonSpacing,
	ShowerSpacing=                  ShowerSpacing,
	Boundary=                       Boundary,
	Pulses=                         Pulses,
	ExcludedDOMs=                   [BadDOMsList],
	SeedTrack=                      seed_id,
	Output=                         millipede_id,
	If=                             If and (lambda frame: seed_id in frame))

tray.AddSegment(Blumefit, 'MuBlumefit',
                If = lambda frame : frame.Stop == frame.Physics)


@traysegment
def DeleteAll(tray, name,
             If=lambda frame: True):
  global pt_tup, delete_keys
  for i in xrange(len(pt_tup)):
    for j in xrange(num_mins):
      seed_id = 'Seed'+'%i%i' % (i,j)
      millipede_id = 'Milli_'+'%i%i' % (i,j)
      millipedefp_id = 'Milli_'+'%i%i' % (i,j) +'FitParams'
      delete_keys.append(seed_id)  
      delete_keys.append(millipede_id)  
      delete_keys.append(millipedefp_id)  
  tray.Add('Delete', 'All_delete', Keys=delete_keys)

tray.Add(BestFit)

#tray.Add(DeleteAll)

tray.Add("I3Writer",
  DropOrphanStreams = [icetray.I3Frame.DAQ],
  filename=sys.argv[3])


tray.Execute(100)
