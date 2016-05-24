import matplotlib
matplotlib.use('Agg')
import numpy,pylab
from matplotlib import rcParams
from matplotlib import colors, ticker, cm
import matplotlib.pyplot as plt
import cPickle as pickle  
import sys
import math

in_file = pickle.load(open(sys.argv[1],'rb'))
print 'Expected Events:',in_file['result']['expected_events']
print 'Norm:',in_file['result']['norm'],'Theta23:',in_file['result']['theta23'],'DM31:',in_file['result']['dm31'],'Norm E:',in_file['result']['norm_e'],'Gamma:',in_file['result']['gamma'],'Dom Eff:',in_file['result']['domeff'],'Hole Ice:',in_file['result']['hole_ice'],'Atm. Mu Frac:',in_file['result']['atmmu_fraction']
