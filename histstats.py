import numpy
import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import pylab
import cPickle as pickle
import glob
import math 

#TODO explore this mystery
#z_space = numpy.linspace(-1,0,9)
#e_space = numpy.linspace(6,56,9)
#z_space = numpy.arccos(numpy.linspace(-1,0.,9))[::-1]
z_space = numpy.arccos(numpy.linspace(-1,0,9))[::-1]
e_space = 10**numpy.linspace(0.8,1.75,9)
in_list = glob.glob(sys.argv[1])
print in_list
print z_space,e_space
tot_counts = numpy.zeros((len(e_space)-1,len(z_space)-1))
tot_scounts = numpy.zeros((len(e_space)-1,len(z_space)-1))
for in_file in in_list:
  p_file = pickle.load(open(in_file,'rb'))
  #MC
#  counts,bins,patches = numpy.histogram2d(p_file['CC']['reco_energy'],p_file['CC']['reco_zenith'],[e_space,z_space],weights=p_file['CC']['weight_muj12'])
#  scounts,sbins,spatches = numpy.histogram2d(p_file['CC']['reco_energy'],p_file['CC']['reco_zenith'],[e_space,z_space],weights=p_file['CC']['weight_muj12']*p_file['CC']['weight_muj12'])
  counts,bins,patches = numpy.histogram2d(p_file['CC']['energy'],p_file['CC']['zenith'],[e_space,z_space],weights=p_file['CC']['weight_muj12'])
  scounts,sbins,spatches = numpy.histogram2d(p_file['CC']['energy'],p_file['CC']['zenith'],[e_space,z_space],weights=p_file['CC']['weight_muj12']*p_file['CC']['weight_muj12'])
  tot_counts+=counts
  tot_scounts+=scounts
  #Data
  #counts,bins,patches = numpy.histogram2d(p_file['reco_energy'],p_file['reco_zenith'],[e_space,z_space])
print (((tot_counts*tot_counts)/tot_scounts)).astype(int)


