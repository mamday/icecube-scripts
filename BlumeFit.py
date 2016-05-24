#!/usr/bin/env python

import icecube
from icecube import icetray, dataio, dataclasses, millipede
from icecube.icetray import traysegment

import numpy, os, sys, math

#Things stolen from IgelFit
#from icecube.igelfit.igel import *
import recos
from recos import gulliver_commons

from I3Tray import *

geofile = dataio.I3File(sys.argv[1])
gFrame = geofile.pop_frame()

geometry_ = gFrame["I3Geometry"]

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
MuonPhotonicsService = 'MuonSplinePhotonicsService'
CascadePhotonicsService = 'CascadeSplinePhotonicsService'

#Useful functions
def makeSeed(vertSeed,zen,azi):
  partPos = vertSeed.pos
  partDir = dataclasses.I3Direction(zen,azi)
  partTime = vertSeed.time
  partLength = vertSeed.length
  partShape = dataclasses.I3Particle.ParticleShape.InfiniteTrack

  seedPart = dataclasses.I3Particle(partPos,partDir,partTime,partShape,partLength)

  return seedPart

def enum(**enums):
    return type('Enum', (), enums)

tray = I3Tray()

topleveldir = '/data/sim/sim-new/ice/photonics-mie-ZeroLengthMuons/'
topleveldir1 = '/data/user/mntobin/IceRec/Tables/'
spline_tables = enum(
                PhotoSplineAmplitudeTableCscd   = topleveldir1 + '/ems_mie_z20_a10_150.abs.fits',
                PhotoSplineTimingTableCscd      = topleveldir1 + '/ems_mie_z20_a10_150.prob.fits',
                PhotoSplineAmplitudeTableMuon   = topleveldir + '/ZeroLengthMieMuons_150_z20_a10.abs.fits',
                PhotoSplineTimingTableMuon      = topleveldir + '/ZeroLengthMieMuons_150_z20_a10.prob.fits')

gulliver_commons(tray, spline_tables, photonics=False)

#Start tray
def GetKinVals(frame,place):
    dx = 0
    dy = 0
    dz = 0
    direction_seedmap = [ (2.895, 326.508), (15.672, 162.173), (16.767, 87.737), (18.129, 229.531), (19.722, 26.743), (21.298, 330.356), (23.698, 281.026), (28.827, 125.710), (31.061, 196.084), (34.125, 359.745), (34.318, 161.840), (34.513, 74.688), (36.617, 228.496), (36.623, 42.977), (39.431, 320.570), (39.878, 258.007), (41.991, 286.490), (43.931, 107.588), (45.736, 139.059), (47.193, 19.992), (47.461, 181.905), (48.162, 207.024), (49.125, 343.152), (50.498, 60.924), (51.610, 84.793), (54.236, 305.186), (54.818, 159.996), (55.054, 229.122), (57.401, 39.527), (57.517, 273.028), (57.653, 251.102), (58.547, 122.045), (59.240, 2.276), (61.120, 325.560), (63.448, 101.669), (64.816, 141.974), (65.174, 197.997), (65.622, 177.720), (66.515, 21.331), (67.513, 290.510), (68.553, 56.038), (68.612, 344.275), (70.256, 82.903), (70.463, 217.280), (71.816, 237.675), (72.318, 309.569), (73.205, 159.667), (75.461, 256.591), (75.848, 38.162), (76.894, 124.772), (77.745, 1.153), (78.929, 275.381), (79.323, 328.637), (81.836, 99.225), (82.525, 68.660), (82.990, 203.303), (83.230, 142.442), (83.619, 183.084), (84.748, 18.512), (85.156, 295.863), (86.650, 226.503), (87.640, 345.340), (89.007, 51.396), (89.967, 244.626), (90.305, 313.727), (91.619, 159.032), (92.353, 114.548), (92.595, 84.163), (92.953, 263.092), (94.871, 33.936), (96.016, 3.708), (96.424, 281.216), (98.532, 330.262), (98.538, 132.156), (98.858, 212.697), (98.880, 193.912), (100.627, 65.667), (100.745, 175.297), (103.470, 99.489), (104.156, 232.650), (106.136, 347.694), (107.120, 47.948), (107.186, 149.017), (107.497, 251.486), (108.294, 309.776), (110.604, 117.281), (110.972, 81.944), (111.262, 25.152), (111.858, 270.743), (112.577, 290.622), (114.551, 5.272), (116.000, 186.422), (116.676, 218.117), (117.133, 327.713), (117.249, 165.794), (119.897, 63.479), (120.573, 134.659), (121.799, 238.553), (124.231, 40.068), (124.687, 347.503), (126.739, 306.960), (127.666, 91.105), (127.826, 259.967), (129.131, 114.754), (129.206, 201.995), (129.770, 17.963), (130.005, 283.609), (132.239, 152.431), (133.257, 177.853), (136.254, 328.457), (137.161, 224.991), (138.137, 70.215), (141.720, 357.397), (142.669, 41.947), (144.044, 130.683), (144.611, 300.635), (145.476, 268.121), (145.549, 98.300), (147.597, 199.267), (149.391, 163.157), (154.675, 235.391), (154.903, 331.643), (156.532, 66.760), (157.074, 17.965), (161.884, 119.272), (162.990, 283.154), (165.667, 188.203), (175.463, 26.215) ]
#Save the llh for all Igelfits in the file
    content_map = []
    for zen, azi in direction_seedmap:
      millipede_id = 'Igelfit_0000' + '_%im_%im_%im_%ideg_%ideg' % (dx, dy, dz, zen, azi)
      if not frame.Has(millipede_id):
        print "WARNING: Skipping igelfit in event %s" % millipede_id
        continue
      millipede = frame[millipede_id]
      millipede_fitparams = frame[millipede_id + 'FitParams']
      rlogl = millipede_fitparams.rlogl
      content_map.append([rlogl, millipede_id])
    if(len(content_map)==0):
      return 0,0,0
#Find the num_mins values of energy,zenith and azimuth
    if(place==1):
      fit = min(content_map, key= lambda content_map : content_map[0])
    else:
      for i in xrange(place-1):
        content_map.remove(min(content_map, key= lambda content_map : content_map[0]))
      fit = min(content_map, key= lambda content_map : content_map[0])
    fit_rlogl = fit[0]
    fit_id = fit[1]
    track_fit = frame[fit_id]
    track_fit_fitparams = frame[fit_id + 'FitParams']
    zenith, azimuth, energy = track_fit[0].dir.zenith, track_fit[0].dir.azimuth, 0.
    for bin in track_fit : energy += bin.energy
    return energy,zenith,azimuth
 


def Seeder(frame):
  global pt_tup
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
  content_map = []
  igel_seed = frame[vert_seed]
#  for i in xrange(len(pt_tup)):
#    for j in xrange(num_mins):
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

#Run tray and make tray segments
tray.Add("I3Reader",Filenamelist=[sys.argv[1],sys.argv[2]])

tray.Add(Seeder)

@traysegment
def Blumefit(tray, name,
             If=lambda frame: True):
  
#  for i in xrange(len(pt_tup)):
#    for j in xrange(num_mins):
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


tray.Execute()
