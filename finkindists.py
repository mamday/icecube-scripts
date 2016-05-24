import numpy

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import pylab

data_hist = numpy.array([[  13.,    9.,   14.,   14.,   21.,   23.,   36.,   53.],
 [  22.,   23.,   28.,   28.,   34.,   33.,   58.,   76.],
 [  40.,   60.,   52.,   45.,   44.,   44.,   76.,   84.],
 [  84.,   80.,   68.,   69.,   72.,   85.,   76.,   98.],
 [ 102.,  109.,  112.,  112.,   83.,   70.,   81.,   94.],
 [ 128.,  146.,  139.,  114.,   94.,   74.,   82.,   84.],
 [ 119.,  140.,  148.,  139.,  116.,  104.,   72.,   95.],
 [ 151.,  164.,  155.,  141.,  143.,  116.,   87.,   98.]]
)

#inj_hist=numpy.array([[   8.44,   10.25,   11.83,   13.72,   21.32,   24.22,   35.57,   47.87],
# [  23.81,   22.44,   29.75,   30.66,   33.99,   39.38,   58.63,   76.69],
# [  44.29,   52.21,   50.56,   50.15,   52.26,   54.73,   70.97,   96.52], 
# [  77.46,   80.51,   79.42,   76.78,   72.48,   69.84,   72.76,  102.84], 
# [  98.78,  113.98,  108.57,   96.44,   86.44,   73.22,   77.32,   88.55], 
# [ 110.66,  134.06,  123.33,  120.61,  101.42,   83.16,   80.88,   85.08], 
# [ 135.65,  160.31,  155.62,  138.07,  130.26,  103.44,   88.13,   79.56],
# [ 135.78,  159.15,  156.69,  148.73,  134.86,  117.9,    93.57,   87.43]])
#data_hist=numpy.array([[7.24,    8.53,   10.08,   13.28,   19.41,   25.62,   32.86,   45.29],
#[20.86,   24.26,   25.39,   27.72,   34.58,   41.32,   58.02,   75.31],
#[41.39,   45.89,   48.22,   48.61,   54.42,   56.88,   75.81,   96.71],
#[72.51,   80.78,   75.47,   70.96,   65.75,   66.6,    77.86,  102.43],
#[102.28,  112.78,  109.28,   92.73,   86.39,   80.3,    73.08,   90.59],
#[115.14,  131.84,  128.41,  113.5,   105.13,   86.1,    74.13,   86.09],
#[134.8,   153.1,   155.6,   135.66,  126.31,  103.15,   92.09,   90.61],
#[130.2,   160.24,  156.04,  149.04,  139.37,  120.76,   91.96,   97.22]])

inj_hist=numpy.array([[7.32,    8.68,   10.25,   13.47,   19.72,   26.25,   32.84,   44.53],
[21.07,   24.65,   25.82,   28.08,   35.04,   42.4,    58.96,   75.93],
[41.58,   45.73,   48.81,   48.6,    55.05,   58.71,   78.42,  100.87],
[72.96,   81.24,   74.76,   71.47,   66.41,   68.87,   81.15,  110.85],
[103.38,  114.46,  109.91,   92.27,   86.96,   81.89,   77.52,  101.73],
[115.99,  131.99,  127.65,  112.34,  103.05,   85.15,   76.28,   92.72],
[135.7,   152.8,   155.47,  133.5,   122.1,    98.47,   88.73,   85.77],
[130.98,  160.53,  155.25,  145.34,  133.98,  114.86,   84.55,   82.17]])

print data_hist
print inj_hist

z_space = numpy.linspace(-1,0,9)
e_space = numpy.linspace(6,56,9)
z_bincent = numpy.zeros(8)
e_bincent = numpy.zeros(8)
for ind,val in enumerate(z_space):
  if val>-1:
    z_bincent[ind-1] = 0.5*(z_space[ind]+z_space[ind-1])
    e_bincent[ind-1] = 0.5*(e_space[ind]+e_space[ind-1])
tot_zdat = numpy.zeros(8) 
tot_zinj = numpy.zeros(8) 
tot_einj = numpy.zeros(8) 
tot_edat = numpy.zeros(8) 
for ind,z_bins in enumerate(data_hist):
#  matplotlib.pyplot.plot(z_bincent,z_bins,marker='o',color='k')
  tot_zdat = tot_zdat + z_bins
  tot_zinj = tot_zinj + inj_hist[ind] 
  tot_edat[ind] = sum(z_bins)
  tot_einj[ind] = sum(inj_hist[ind])
  matplotlib.pyplot.plot(z_bincent,inj_hist[ind])
  pyplot.errorbar(
    z_bincent,
    z_bins,
    color='k',
    yerr = z_bins**0.5,
    marker = 'o',
    drawstyle = 'steps-mid-'
  )
  pylab.xlabel("Cos(zenith)")
  pylab.ylabel("Events")
  pylab.ylim(0,210)
  pylab.savefig("DataMCComp%s.png" % ind)
  matplotlib.pyplot.close()
  if(ind==7):
    matplotlib.pyplot.plot(z_bincent,tot_zinj,'r')
    matplotlib.pyplot.plot(z_bincent,tot_zdat,'b')
    pylab.xlabel("cos(zenith)")
    pylab.ylabel("Events")
    pylab.savefig("DataMCCompZTot.png")
    matplotlib.pyplot.close()
#    pyplot.errorbar(
#      z_bincent,
#      tot_zdat,
#      color='k',
#      yerr = tot_zdat**0.5,
#      marker = 'o',
#      drawstyle = 'steps-mid-'
#    )
#    pylab.xlabel("Cos(zenith)")
    print tot_einj
    print tot_edat
    print tot_zinj
    print tot_zdat
    matplotlib.pyplot.plot(e_bincent,tot_einj,color='r')
    matplotlib.pyplot.plot(e_bincent,tot_edat,color='b')
    pylab.xlabel("Energy (GeV)")
    pylab.ylabel("Events")
    pylab.savefig("DataMCCompETot.png")
    matplotlib.pyplot.close()
