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

#MT=0
inj_hist = numpy.array([[   7.33,    8.98,   11.05,   14.4 ,   19.78,   26.21,   33.6 ,   43.98],
       [  21.77,   25.79,   27.  ,   29.29,   36.07,   43.27,   58.11,   74.47],
       [  43.12,   48.45,   49.68,   50.61,   55.65,   58.94,   75.56,   95.97],
       [  74.26,   82.96,   76.03,   72.89,   66.83,   68.17,   78.45,  102.47],
       [ 105.98,  116.05,  110.69,   92.64,   86.58,   78.7 ,   71.3 ,   88.69],
       [ 115.83,  133.89,  129.64,  113.5 ,  103.33,   84.84,   71.18,   81.85],
       [ 136.39,  154.6 ,  154.47,  136.28,  124.24,   99.63,   87.11,   84.36],
       [ 130.91,  159.84,  157.83,  147.99,  137.86,  116.12,   88.97,   91.56]])

#MT=0.006
inj_hist1 = numpy.array([[   7.38,    9.11,   11.19,   14.56,   20.1 ,   26.68,   33.65,   44.03],
       [  21.97,   26.09,   27.35,   29.59,   36.43,   44.08,   59.01,   75.51],
       [  43.33,   48.43,   50.21,   50.67,   56.2 ,   60.16,   77.32,   98.91],
       [  74.7 ,   83.47,   75.83,   73.42,   67.22,   69.53,   80.41,  106.73],
       [ 106.94,  117.35,  111.31,   92.48,   86.95,   79.24,   73.24,   92.98],
       [ 116.62,  134.21,  129.45,  112.92,  102.06,   83.99,   71.31,   82.95],
       [ 137.24,  154.69,  154.79,  135.26,  122.02,   96.89,   84.86,   79.41],
       [ 131.65,  160.35,  157.69,  146.23,  135.16,  113.05,   85.02,   82.47]])
#MT=0.015
inj_hist2 = numpy.array([[   7.33,    9.15,   11.18,   14.47,   20.12,   26.67,   32.98,   42.45],
       [  21.86,   25.95,   27.25,   29.55,   36.24,   44.24,   57.95,   74.03],
       [  42.78,   47.55,   50.24,   50.18,   55.97,   61.15,   77.98,   99.23],
       [  74.03,   82.65,   74.15,   73.17,   67.94,   71.71,   82.9 ,  113.85],
       [ 106.36,  117.2 ,  110.66,   91.36,   87.91,   82.18,   79.99,  109.13],
       [ 115.99,  132.72,  127.1 ,  110.89,  100.6 ,   85.51,   78.71,  100.9 ],
       [ 136.37,  152.76,  152.72,  131.26,  117.03,   93.27,   85.27,   87.86],
       [ 130.65,  158.58,  154.96,  140.34,  127.84,  106.54,   79.06,   75.38]])
#MT=-0.006
inj_hist3 = numpy.array([[   7.21,    8.79,   10.82,   14.09,   19.27,   25.42,   33.07,   42.87],
       [  21.35,   25.2 ,   26.4 ,   28.75,   35.32,   42.03,   56.01,   71.98],
       [  42.47,   47.89,   48.82,   50.17,   54.57,   57.4 ,   73.11,   91.73],
       [  73.13,   81.65,   75.41,   71.89,   66.54,   67.08,   76.61,  100.13],
       [ 104.07,  113.78,  109.34,   92.44,   86.63,   79.46,   72.05,   91.44],
       [ 114.18,  132.55,  128.74,  113.54,  104.75,   87.17,   75.04,   90.36],
       [ 134.36,  153.31,  153.04,  136.04,  125.48,  102.3 ,   91.15,   95.87],
       [ 129.05,  157.96,  156.61,  147.78,  138.58,  117.72,   91.97,  100.07]])

#MT=-0.015
inj_hist4 = numpy.array([[   6.97,    8.47,   10.39,   13.5 ,   18.38,   23.97,   31.61,   40.06],
       [  20.53,   24.09,   25.36,   27.76,   33.77,   39.97,   51.86,   67.26],
       [  41.02,   46.33,   47.37,   49.14,   52.58,   55.09,   69.5 ,   85.92],
       [  70.76,   78.92,   73.64,   70.29,   66.72,   66.63,   75.15,  101.05],
       [ 100.56,  109.73,  106.87,   92.34,   87.99,   83.08,   77.82,  104.84],
       [ 110.98,  129.52,  126.32,  113.22,  107.23,   92.88,   85.85,  112.67],
       [ 129.99,  149.87,  150.  ,  134.27,  125.97,  105.81,   98.73,  114.89],
       [ 125.08,  153.54,  153.08,  144.54,  136.66,  117.35,   93.46,  104.81]])

#MT Fixed
inj_hist5 = numpy.array([[   7.34,    8.9 ,   10.79,   14.09,   19.66,   25.94,   33.36,   44.17],
       [  21.46,   25.48,   26.68,   28.75,   35.3 ,   42.49,   57.93,   74.64],
       [  42.69,   48.1 ,   49.27,   50.1 ,   54.79,   57.67,   74.7 ,   94.91],
       [  73.85,   82.54,   76.2 ,   72.48,   66.12,   66.81,   76.96,  100.92],
       [ 104.5 ,  115.39,  110.86,   93.27,   86.42,   78.92,   71.25,   88.4 ],
       [ 115.04,  133.35,  129.8 ,  114.3 ,  104.22,   85.81,   72.7 ,   83.57],
       [ 135.24,  154.17,  154.75,  136.55,  125.37,  101.32,   89.59,   88.05],
       [ 129.67,  159.42,  157.19,  148.15,  138.  ,  117.83,   90.95,   94.85]]) 

z_space = numpy.linspace(0,-1,9)
e_space = numpy.linspace(6,56,9)
z_bincent = numpy.zeros(8)
e_bincent = numpy.zeros(8)
for ind,val in enumerate(z_space):
  if val<0:
    z_bincent[ind-1] = 0.5*(z_space[ind]+z_space[ind-1])
    e_bincent[ind-1] = 0.5*(e_space[ind]+e_space[ind-1])
tot_zdat = numpy.zeros(8) 
tot_zinj = numpy.zeros(8) 
tot_zinj1 = numpy.zeros(8) 
tot_zinj2 = numpy.zeros(8) 
tot_zinj3 = numpy.zeros(8) 
tot_zinj4 = numpy.zeros(8) 
tot_zinj5 = numpy.zeros(8) 
tot_einj = numpy.zeros(8) 
tot_einj1 = numpy.zeros(8) 
tot_einj2 = numpy.zeros(8) 
tot_einj3 = numpy.zeros(8) 
tot_einj4 = numpy.zeros(8) 
tot_einj5 = numpy.zeros(8) 
tot_edat = numpy.zeros(8) 
for ind,z_bins in enumerate(data_hist):
  matplotlib.pyplot.plot(z_bincent,z_bins,marker='o',color='k')
  tot_zdat = tot_zdat + z_bins
  tot_zinj = tot_zinj + inj_hist[ind] 
  tot_zinj1 = tot_zinj1 + inj_hist1[ind] 
  tot_zinj2 = tot_zinj2 + inj_hist2[ind] 
  tot_zinj3 = tot_zinj3 + inj_hist3[ind] 
  tot_zinj4 = tot_zinj4 + inj_hist4[ind] 
  tot_zinj5 = tot_zinj5 + inj_hist5[ind] 
  tot_edat[ind] = sum(z_bins)
  tot_einj[ind] = sum(inj_hist[ind])
  tot_einj1[ind] = sum(inj_hist1[ind])
  tot_einj2[ind] = sum(inj_hist2[ind])
  tot_einj3[ind] = sum(inj_hist3[ind])
  tot_einj4[ind] = sum(inj_hist4[ind])
  tot_einj5[ind] = sum(inj_hist5[ind])
  matplotlib.pyplot.plot(z_bincent,inj_hist[ind],'r',label=r'$\epsilon_{\mu \tau}=0.0$')
  #matplotlib.pyplot.plot(z_bincent,inj_hist1[ind],'orange',label=r'$\epsilon_{\mu \tau}=0.006$')
  #matplotlib.pyplot.plot(z_bincent,inj_hist2[ind],'b',label=r'$\epsilon_{\mu \tau}=0.015$')
  #matplotlib.pyplot.plot(z_bincent,inj_hist3[ind],'g',label=r'$\epsilon_{\mu \tau}=-0.006$')
  #matplotlib.pyplot.plot(z_bincent,inj_hist4[ind],'lightblue',label=r'$\epsilon_{\mu \tau}=-0.015$')
  matplotlib.pyplot.plot(z_bincent,inj_hist5[ind],'violet',label=r'$\epsilon_{\mu \tau}$ Fixed')
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
  pylab.legend(loc=2,ncol=2)
  pylab.savefig("FinMDataMCComp%s.png" % ind)
  matplotlib.pyplot.close()
  if(ind==7):
    matplotlib.pyplot.plot(z_bincent,tot_zinj,'r',label=r'$\epsilon_{\mu \tau}=0.0$')
    #matplotlib.pyplot.plot(z_bincent,tot_zinj1,'orange',label=r'$\epsilon_{\mu \tau}=0.006$')
    #matplotlib.pyplot.plot(z_bincent,tot_zinj2,'b',label=r'$\epsilon_{\mu \tau}=0.015$')
    #matplotlib.pyplot.plot(z_bincent,tot_zinj3,'g',label=r'$\epsilon_{\mu \tau}=-0.006$')
    #matplotlib.pyplot.plot(z_bincent,tot_zinj4,'lightblue',label=r'$\epsilon_{\mu \tau}=-0.015$')
    matplotlib.pyplot.plot(z_bincent,tot_zinj5,'violet',label=r'$\epsilon_{\mu \tau}$ Fixed')
    matplotlib.pyplot.plot(z_bincent,tot_zdat,'k')
    pylab.xlabel("cos(zenith)")
    pylab.ylabel("Events")
    pylab.legend(ncol=2,loc=3)
    pylab.savefig("FinMDataMCCompZTot.png")
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
    matplotlib.pyplot.plot(e_bincent,tot_einj,color='r',label=r'$\epsilon_{\mu \tau}=0.0$')
    #matplotlib.pyplot.plot(e_bincent,tot_einj1,color='orange',label=r'$\epsilon_{\mu \tau}=0.006$')
    #matplotlib.pyplot.plot(e_bincent,tot_einj2,color='b',label=r'$\epsilon_{\mu \tau}=0.015$')
    #matplotlib.pyplot.plot(e_bincent,tot_einj3,color='g',label=r'$\epsilon_{\mu \tau}=-0.006$')
    #matplotlib.pyplot.plot(e_bincent,tot_einj4,color='lightblue',label=r'$\epsilon_{\mu \tau}=-0.015$')
    matplotlib.pyplot.plot(e_bincent,tot_einj5,color='violet',label=r'$\epsilon_{\mu \tau}$ Fixed')
    matplotlib.pyplot.plot(e_bincent,tot_edat,color='k')
    pylab.xlabel("Energy (GeV)")
    pylab.ylabel("Events")
    pylab.legend(ncol=2,loc=2)
    pylab.savefig("FinMDataMCCompETot.png")
    matplotlib.pyplot.close()
