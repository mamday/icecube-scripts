import numpy

import matplotlib
matplotlib.use('Agg')
from matplotlib import cm,pyplot
import pylab
import math

data_hist = numpy.array([[  13.,    9.,   14.,   14.,   21.,   23.,   36.,   53.],
 [  22.,   23.,   28.,   28.,   34.,   33.,   58.,   76.],
 [  40.,   60.,   52.,   45.,   44.,   44.,   76.,   84.],
 [  84.,   80.,   68.,   69.,   72.,   85.,   76.,   98.],
 [ 102.,  109.,  112.,  112.,   83.,   70.,   81.,   94.],
 [ 128.,  146.,  139.,  114.,   94.,   74.,   82.,   84.],
 [ 119.,  140.,  148.,  139.,  116.,  104.,   72.,   95.],
 [ 151.,  164.,  155.,  141.,  143.,  116.,   87.,   98.]]
)
and_nc_data_hist = numpy.array([[  21.,   13.1,   18.,   18.,   25.,   25.1,   40.,   52.],
       [  24.,   35.,   35.,   35.,   48.,   35.,   57.,   72.],
       [  49.,   70.,   61.,   54.,   47.,   52.,   76.,   83.],
       [ 104.,  103.,   84.,   83.,   86.,   95.,   86.,   90.],
       [ 122.,  124.,  130.,  129.,   92.,   76.,   87.,   86.],
       [ 135.,  158.,  149.,  129.,  106.,   76.,   85.,   82.],
       [ 135.,  157.,  157.,  147.,  128.,  106.,   69.,   91.],
       [ 156.,  180.,  180.,  152.,  155.,  118.,   88.,  103.]]) 

and_nc_mc_hist = numpy.array([[  11.66,   13.91,   14.51,   19.5 ,   24.61,   29.52,   39.25,   47.99],
       [  25.8 ,   31.19,   33.24,   38.22,   44.69,   52.74,   59.44,   74.26],
       [  49.4 ,   59.04,   58.52,   63.53,   62.89,   63.01,   74.97,   91.21],
       [  83.31,  101.34,   90.93,   85.05,   77.57,   77.74,   78.23,   94.96],
       [ 105.4 ,  118.84,  113.88,  101.16,   93.79,   72.35,   67.85,   81.57],
       [ 117.6 ,  139.56,  129.28,  114.07,  105.24,   76.47,   68.01,   66.95],
       [ 123.28,  150.68,  142.72,  132.72,  118.47,   90.55,   72.58,   68.37],
       [ 128.07,  148.92,  147.62,  129.23,  124.07,  101.04,   79.15,   72.3 ]])  

andmc_hist = numpy.array([[  11.71,   13.88,   14.58,   20.28,   24.93,   29.88,   39.62,   49.2 ],
       [  25.81,   31.48,   33.67,   38.49,   44.02,   53.36,   59.56,   75.46],
       [  49.96,   59.4 ,   58.41,   63.89,   63.08,   63.09,   75.93,   91.4 ],
       [  84.1 ,  101.63,   91.53,   85.83,   75.84,   79.49,   79.78,   95.69],
       [ 105.09,  120.09,  113.36,  100.67,   93.11,   73.98,   67.95,   82.31],
       [ 117.03,  139.31,  129.89,  113.97,  104.41,   76.45,   68.71,   67.09],
       [ 120.9 ,  147.84,  140.38,  131.11,  116.36,   91.57,   73.37,   68.08],
       [ 125.45,  145.99,  145.58,  127.93,  124.78,  101.77,   80.51,   74.  ]])  


anddata_hist = numpy.array([[  20.,   13.,   17.,   17.,   24.,   25.,   38.,   48.],
       [  23.,   30.,   33.,   32.,   43.,   34.,   53.,   69.],
       [  48.,   64.,   57.,   48.,   45.,   48.,   68.,   77.],
       [  93.,   91.,   76.,   76.,   75.,   84.,   77.,   83.],  
       [ 107.,  111.,  116.,  120.,   78.,   68.,   77.,   80.],
       [ 116.,  142.,  129.,  125.,   97.,   70.,   74.,   72.],
       [ 120.,  134.,  145.,  127.,  119.,   93.,   63.,   83.],
       [ 137.,  161.,  154.,  145.,  142.,  104.,   82.,   98.]])
print 'Hists',and_nc_data_hist,anddata_hist
mc_diff = 1-((and_nc_mc_hist-andmc_hist)/and_nc_mc_hist)
data_diff = 1-((and_nc_data_hist-anddata_hist)/and_nc_data_hist)
print 'Diffs',mc_diff,data_diff
print 'Ratio Hist',mc_diff/data_diff 
print 'Mult diff',mc_diff*and_nc_mc_hist
print 'Such fun good times',(and_nc_data_hist-anddata_hist)/and_nc_data_hist
abs_diff = (and_nc_data_hist-anddata_hist) 
print 'Avg',sum([j for i in (and_nc_data_hist-anddata_hist)/and_nc_data_hist for j in i])/len([j for i in (and_nc_data_hist-anddata_hist)/and_nc_data_hist for j in i])
avg = sum([j for i in (and_nc_data_hist-anddata_hist)/and_nc_data_hist for j in i])/len([j for i in (and_nc_data_hist-anddata_hist)/and_nc_data_hist for j in i])
avg_diff = sum([j for i in (and_nc_data_hist-anddata_hist) for j in i])/len([j for i in (and_nc_data_hist-anddata_hist) for j in i]) 
rel_res = abs_diff-avg_diff
abs_res = rel_res/avg_diff 
print 'Abs Diffs',abs_diff
print 'Avg Diff', avg_diff
print 'Rel Res',rel_res
print 'Abs Res',abs_res
xr = numpy.linspace(0,-1,9)
yr = numpy.linspace(6,56,9)
cs = pylab.pcolormesh(xr,yr,numpy.absolute(rel_res),cmap=cm.RdYlBu)
cbar = pylab.colorbar(cs)
pylab.xlabel("Cos(zenith)")
pylab.ylabel("Energy (GeV)")
pylab.ylim(6,56)
pylab.savefig('RelResAndZCut.png')
pylab.close()

cs = pylab.pcolormesh(xr,yr,numpy.absolute(abs_res),cmap=cm.RdYlBu)
cbar = pylab.colorbar(cs)
pylab.xlabel("Cos(zenith)")
pylab.ylabel("Energy (GeV)")
pylab.ylim(6,56)
pylab.savefig('AbsResAndZCut.png')
pylab.close()

diff = (and_nc_data_hist-anddata_hist)/and_nc_data_hist  
print 'Deviation good times', (diff - avg)
std_dev = sum([j for i in (diff - avg)*(diff-avg) for j in i])/len([j for i in (diff - avg)*(diff-avg) for j in i])
print 'Std. Dev.',math.sqrt(std_dev)
diff2 = diff-avg
print 'Abs ZScore', numpy.absolute(diff-avg)/math.sqrt(std_dev)
cs = pylab.pcolormesh(xr,yr,numpy.absolute(diff-avg)/math.sqrt(std_dev),cmap=cm.RdYlBu)
cbar = pylab.colorbar(cs)
pylab.xlabel("Cos(zenith)")
pylab.ylabel("Energy (GeV)")
pylab.ylim(6,56)
pylab.savefig('ZScoreAndZCut.png')
pylab.close()
print 'G1sigma',[j for i in (diff-avg) for j in i if math.fabs(j)>math.sqrt(std_dev)],len([j for i in (diff-avg) for j in i if math.fabs(j)>math.sqrt(std_dev)])
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
