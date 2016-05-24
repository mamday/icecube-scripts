#!/usr/bin/env python

"""
Use muon flux weights to calculate an effective livetime for combined
CORSIKA samples as a function of energy.
"""

import pylab, numpy
from icecube import MuonGun, icetray,dataclasses
from icecube.icetray import I3Units

outer = MuonGun.Cylinder(1600, 800)
#inner = MuonGun.Cylinder(1600, 800)
inner = MuonGun.Cylinder(500, 150, dataclasses.I3Position(46.3,-34.9,-300))
#inner = MuonGun.Cylinder(700, 125, dataclasses.I3Position(29.3,52.6,-150))
#inner = outer
#Most tested spectrum
#spectrum = MuonGun.OffsetPowerLaw(5.0, 7e2, 0, 1e5)
spectrum = MuonGun.OffsetPowerLaw(5.0, 7e2, 500, 1e5)

#Limited spectrum range
#spectrum = MuonGun.OffsetPowerLaw(5.2, 7e2, 150, 1e4)
#spectrum = MuonGun.OffsetPowerLaw(2, 1*I3Units.TeV, 1*I3Units.TeV, 1*I3Units.PeV)
#Good spectrum producing ~1 day with 10k evts above 200 GeV
#spectrum = MuonGun.OffsetPowerLaw(5.2, 7e2, 200, 1e6)
#Jackob's spectrum
#spectrum = MuonGun.OffsetPowerLaw(5.0, 5e2, 200, 1e6)
#Good spectrum producing ~1 day with 5000 evts above 400 GeV
#spectrum = MuonGun.OffsetPowerLaw(5.25, 1000, 1, 1e6)
model = MuonGun.load_model('/home/mamday/icesim/build/MuonGun/resources/tables/GaisserH4a_atmod12_SIBYLL')
#gun = .365e4*MuonGun.EnergyDependentSurfaceInjector(outer, model.flux, spectrum, model.radius,

gun = 5000*MuonGun.EnergyDependentSurfaceInjector(outer, model.flux, spectrum, model.radius,

#gun = 680*MuonGun.EnergyDependentSurfaceInjector(outer, model.flux, spectrum, model.radius,
    MuonGun.ConstantSurfaceScalingFunction(inner))

def get_weight(weighter, energy, zenith=numpy.pi/8, scale=True):
# def get_weight(weighter, energy, zenith=0, z=0):	
	shape = energy.shape
	if scale:
		x = numpy.array([gun.target_surface(e).radius - 1 for e in energy])
	else:
		# x = numpy.ones(shape[0])*surface.radius - 1
		x = numpy.ones(shape[0])*surface.radius - 1
	
	# x = surface.radius*numpy.ones(shape) - 1
	y = numpy.zeros(shape)
	# z = z*numpy.ones(shape)
	if scale:
		z = numpy.array([gun.target_surface(e).center.z + gun.target_surface(e).length/2. for e in energy])
	else:
		z = numpy.ones(shape[0])*(surface.center.z + surface.length/2.)
	
	azimuth = numpy.zeros(shape)
        #print azimuth 
       # zenith = 1.47
	zenith = zenith*numpy.ones(shape)
	multiplicity = numpy.ones(shape, dtype=numpy.uint32)
	mmax = multiplicity.max()
	e = numpy.zeros(shape + (mmax,), dtype=numpy.float32)
	e[:,0] = energy
	r = numpy.zeros(shape + (mmax,), dtype=numpy.float32)
	return weighter(x, y, z, zenith, azimuth, multiplicity, e, r)

bins = 101 
e = numpy.logspace(2.0, 5.0, bins)
zbins = numpy.linspace(0, 1.0, bins)

target = MuonGun.load_model('/home/mamday/icesim/build/MuonGun/resources/tables/GaisserH4a_atmod12_SIBYLL')

generators = [
	('5000 MuonGun files, All Zens (10k events)', 1e4*gun)
]

fig = pylab.figure(figsize=(6,4))
fig.subplots_adjust(bottom=0.15)

diem = 24*3600
for label, generator in generators:
	weighter = MuonGun.WeightCalculator(target, generator)
        tot_weight = bins*[0]
        for tzen in zbins:
          tot_weight+=get_weight(weighter, e, zenith=tzen, scale=True)
          #print 'Ha',tzen,tot_weight,get_weight(weighter, e, zenith=tzen, scale=True)
#	pylab.plot(e, 1./(get_weight(weighter, e, scale=True)*diem), color='r',label='Zen=pi/8')
	pylab.plot(e, 1./((tot_weight/bins)*diem), label=label)
pylab.loglog()
pylab.legend(loc='upper right', prop=dict(size='x-small'))
pylab.ylabel('Single-muon livetime [days]')
pylab.xlabel('Muon energy at sampling surface [GeV]')
pylab.grid()

pylab.show()
