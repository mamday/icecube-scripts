import numpy

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import pylab

#data_hist=numpy.array([[],
#[],
#[],
#[],
#[],
#[],
#[],
#[]])

#Th23=0.816 DM=0.00272 nuSQuIDS
data_hist= numpy.array([[  19.09,   10.29,   12.27,   23.32,   26.83,   20.14,   17.74,   30.26],
       [  36.19,   23.8 ,   13.11,   19.01,   38.17,   55.39,   65.51,   48.32],
       [  57.67,   48.16,   29.51,   16.78,   24.76,   50.64,   94.55,  154.47],
       [  96.05,   70.65,   53.91,   34.3 ,   25.37,   30.37,   55.15,  117.17],
       [ 131.95,  108.75,   96.76,   72.79,   51.34,   31.01,   31.44,   48.88],
       [ 151.62,  135.63,  118.99,  109.7 ,   94.  ,   75.14,   58.5 ,   51.78],
       [ 185.45,  164.91,  152.14,  135.81,  135.62,  128.67,  101.21,  105.74],
       [ 190.69,  182.9 ,  165.51,  163.14,  152.63,  145.74,  130.26,  146.34]])

#Th23=0.58 nuSQuIDS
inj_hist7=numpy.array([[  18.45,   11.05,   13.18,   22.37,   26.05,   21.29,   21.98,   35.04],
       [  34.13,   24.24,   16.23,   21.6 ,   37.91,   52.28,   62.77,   56.07],
       [  53.47,   47.09,   32.61,   23.64,   31.74,   53.46,   89.35,  143.24],
       [  88.35,   66.89,   54.2 ,   41.02,   36.97,   44.44,   64.18,  117.91],
       [ 120.73,  101.29,   93.19,   76.06,   60.84,   47.57,   50.87,   71.71],
       [ 138.3 ,  124.8 ,  112.01,  107.04,   97.34,   84.46,   72.93,   75.46],
       [ 168.89,  151.01,  140.73,  127.7 ,  130.98,  129.28,  107.01,  119.58],
       [ 173.46,  166.9 ,  151.94,  151.04,  143.08,  139.33,  127.04,  148.21]]) 

#MT=0.005
inj_hist = numpy.array([[  19.25,   10.38,   12.45,   23.74,   26.99,   20.57,   17.63,   32.06],
       [  36.5 ,   23.91,   13.22,   19.47,   39.14,   56.22,   65.3 ,   45.41],
       [  58.17,   48.36,   29.39,   17.01,   26.02,   53.15,   96.57,  149.32],
       [  96.89,   71.07,   53.97,   33.88,   25.59,   33.03,   60.98,  127.98],
       [ 133.1 ,  109.31,   96.72,   71.44,   49.72,   30.17,   35.26,   67.67],
       [ 152.99,  136.63,  118.82,  108.39,   90.44,   71.88,   56.97,   57.82],
       [ 187.13,  166.11,  152.54,  135.18,  132.77,  123.04,   95.15,   99.66],
       [ 192.44,  184.36,  166.14,  162.58,  150.22,  141.52,  124.4 ,  129.84]]) 

#MT=0.01
inj_hist1=numpy.array([[  19.17,   10.36,   12.5 ,   23.79,   26.62,   20.85,   18.24,   33.97],
       [  36.36,   23.73,   13.24,   19.81,   39.44,   55.39,   63.05,   46.9 ],
       [  57.95,   47.97,   29.01,   17.37,   27.56,   54.99,   94.53,  129.15],
       [  96.53,   70.6 ,   53.4 ,   33.42,   26.74,   37.63,   67.89,  131.86],
       [ 132.62,  108.49,   95.44,   69.41,   48.59,   32.01,   44.66,   99.85],
       [ 152.49,  135.9 ,  117.03,  105.62,   86.19,   69.75,   59.96,   83.52],
       [ 186.51,  165.21,  150.85,  132.54,  127.96,  116.34,   90.68,  107.71],
       [ 191.81,  183.47,  164.46,  159.48,  145.13,  134.68,  117.  ,  118.6 ]]) 

#Th23=1.0 nuSQuIDS
inj_hist6=numpy.array([[  18.67,   11.46,   13.68,   21.93,   24.35,   19.39,   18.66,   31.36],
       [  34.4 ,   24.71,   16.34,   21.35,   36.61,   50.58,   61.12,   53.18],
       [  53.78,   47.5 ,   33.1 ,   23.03,   30.69,   52.63,   88.78,  141.63],
       [  88.7 ,   67.28,   54.53,   41.11,   36.94,   44.73,   64.51,  117.57],
       [ 121.16,  101.64,   93.58,   76.21,   61.12,   48.32,   51.66,   72.2 ],
       [ 138.75,  125.23,  112.32,  107.39,   97.94,   85.35,   73.83,   76.48],
       [ 169.41,  151.45,  141.14,  128.13,  131.63,  130.16,  107.87,  120.75],
       [ 174.  ,  167.39,  152.38,  151.51,  143.69,  140.03,  127.76,  149.22]]) 

#MT=-0.005
inj_hist2 = numpy.array([[  18.71,   10.08,   11.98,   22.57,   26.16,   19.57,   18.55,   28.98],
       [  35.47,   23.43,   12.92,   18.47,   36.61,   53.01,   63.62,   54.75],
       [  56.51,   47.4 ,   29.36,   16.71,   23.86,   47.66,   88.74,  143.24],
       [  94.11,   69.41,   53.25,   34.66,   26.09,   29.83,   51.05,  102.14],
       [ 129.27,  106.91,   95.62,   73.43,   53.34,   34.4 ,   33.52,   48.22],
       [ 148.5 ,  133.02,  117.63,  109.54,   96.69,   79.21,   64.24,   66.59],
       [ 181.63,  161.73,  149.75,  134.47,  136.37,  132.79,  108.02,  123.94],
       [ 186.76,  179.27,  162.7 ,  161.23,  152.29,  147.03,  133.8 ,  163.15]])

#MT=-0.01
inj_hist3=numpy.array([[  18.18,    9.81,   11.63,   21.59,   25.09,   18.94,   19.95,   28.54],
       [  34.47,   22.88,   12.69,   17.92,   34.66,   49.41,   59.99,   62.65],
       [  54.91,   46.26,   29.04,   16.82,   23.4 ,   44.55,   80.09,  119.27],
       [  91.42,   67.6 ,   52.19,   35.03,   27.7 ,   31.4 ,   49.1 ,   86.83],
       [ 125.58,  104.16,   93.63,   73.52,   55.69,   39.99,   40.95,   64.77],
       [ 144.21,  129.31,  115.13,  108.26,   98.57,   83.85,   73.33,   97.01],
       [ 176.38,  157.2 ,  145.93,  131.63,  135.36,  135.35,  114.84,  148.56],
       [ 181.35,  174.15,  158.32,  157.42,  149.65,  145.68,  134.81,  175.39]])

#DM 0.002
inj_hist4=numpy.array([[  20.51,   12.49,    8.28,    9.45,   18.42,   28.68,   38.93,   34.58],
       [  36.68,   28.1 ,   17.19,   10.91,   13.76,   26.8 ,   57.  ,  102.35],
       [  55.94,   52.88,   39.05,   23.62,   14.85,   13.74,   31.36,   78.89],
       [  90.99,   72.12,   62.14,   50.89,   40.55,   29.24,   20.74,   28.92],
       [ 123.14,  106.4 ,  102.49,   90.2 ,   76.19,   59.36,   48.12,   37.59],
       [ 140.19,  128.5 ,  119.43,  119.55,  115.29,  104.84,   91.23,   89.76],
       [ 170.65,  154.08,  146.06,  135.94,  144.63,  149.17,  128.43,  148.04],
       [ 174.89,  169.22,  155.69,  156.98,  151.75,  151.99,  141.93,  172.21]])  

#DM 0.0034
inj_hist5=numpy.array([[  16.81,   10.49,   21.13,   26.26,   15.79,   20.45,   32.45,   46.63],
       [  33.76,   20.07,   16.78,   36.16,   49.39,   42.02,   34.94,   44.19],
       [  56.51,   41.21,   24.34,   25.59,   54.28,   85.57,  101.27,   89.05],
       [  96.79,   65.21,   44.29,   25.6 ,   34.1 ,   70.6 ,  118.4 ,  186.01],
       [ 135.39,  105.36,   85.5 ,   54.18,   35.57,   29.74,   61.71,  129.74],
       [ 157.34,  136.64,  111.68,   93.14,   69.59,   51.08,   44.87,   58.16],
       [ 193.58,  168.96,  150.79,  127.95,  118.34,  101.63,   73.53,   74.06],
       [ 199.88,  189.67,  168.17,  161.24,  144.95,  130.47,  110.98,  113.95]])  

diff_hist = data_hist-inj_hist
diff_hist1 = data_hist-inj_hist1
diff_hist2 = data_hist-inj_hist2
diff_hist3 = data_hist-inj_hist3
diff_hist4 = data_hist-inj_hist4
diff_hist5 = data_hist-inj_hist5
diff_hist6 = data_hist-inj_hist6
diff_hist7 = data_hist-inj_hist7

z_space = numpy.linspace(0,-1,9)
e_space = numpy.linspace(6,56,9)
z_bincent = numpy.zeros(8)
e_bincent = numpy.zeros(8)

for ind,val in enumerate(z_space):
  if val<0:
    #z_bincent[ind-1] = 0.5*(z_space[ind]+z_space[ind-1])
    #e_bincent[ind-1] = 0.5*(e_space[ind]+e_space[ind-1])
    z_bincent[ind-1] = z_space[ind-1]
    e_bincent[ind-1] = e_space[ind-1]
xx, yy = pylab.meshgrid(
z_space,
e_space
)
print z_bincent 
pylab.pcolor(xx,yy,diff_hist)
cbar = pylab.colorbar()
pylab.xlabel("Cos(zenith)")
pylab.ylabel("Energy (GeV)")
pylab.xlim(-1,0)
pylab.ylim(6,56)
cbar.set_label("#Events Difference from PRD")
pylab.clim(-40,40)
pylab.savefig("KinDiffMTP005Plot.png")
pylab.close()
pylab.pcolor(xx,yy,diff_hist1)
cbar = pylab.colorbar()
pylab.xlabel("Cos(zenith)")
pylab.ylabel("Energy (GeV)")
pylab.xlim(-1,0)
pylab.ylim(6,56)
cbar.set_label("#Events Difference from PRD")
pylab.clim(-40,40)
pylab.savefig("KinDiffMTP01Plot.png")
pylab.close()
pylab.pcolor(xx,yy,diff_hist2)
cbar = pylab.colorbar()
pylab.clim(-40,40)
pylab.xlabel("Cos(zenith)")
pylab.ylabel("Energy (GeV)")
pylab.xlim(-1,0)
pylab.ylim(6,56)
cbar.set_label("#Events Difference from PRD")
pylab.savefig("KinDiffMTMP005P9Plot.png")
pylab.close()
pylab.pcolor(xx,yy,diff_hist3)
cbar = pylab.colorbar()
pylab.xlabel("Cos(zenith)")
pylab.ylabel("Energy (GeV)")
pylab.xlim(-1,0)
pylab.ylim(6,56)
cbar.set_label("#Events Difference from PRD")
pylab.clim(-40,40)
pylab.savefig("KinDiffMTMP01Plot.png")
pylab.close()
pylab.pcolor(xx,yy,diff_hist4)
cbar = pylab.colorbar()
pylab.xlabel("Cos(zenith)")
pylab.ylabel("Energy (GeV)")
pylab.xlim(-1,0)
pylab.ylim(6,56)
cbar.set_label("#Events Difference from PRD")
pylab.clim(-40,40)
pylab.savefig("KinDiffDM002Plot.png")
pylab.close()
pylab.pcolor(xx,yy,diff_hist5)
cbar = pylab.colorbar()
pylab.xlabel("Cos(zenith)")
pylab.ylabel("Energy (GeV)")
pylab.xlim(-1,0)
pylab.ylim(6,56)
cbar.set_label("#Events Difference from PRD")
pylab.clim(-40,40)
pylab.savefig("KinDiffDM0034Plot.png")
pylab.close()
pylab.pcolor(xx,yy,diff_hist6)
cbar = pylab.colorbar()
pylab.xlabel("Cos(zenith)")
pylab.ylabel("Energy (GeV)")
pylab.xlim(-1,0)
pylab.ylim(6,56)
cbar.set_label("#Events Difference from PRD")
pylab.clim(-40,40)
pylab.savefig("KinDiffTh231P0Plot.png")
pylab.close()
pylab.pcolor(xx,yy,diff_hist7)
cbar = pylab.colorbar()
pylab.xlabel("Cos(zenith)")
pylab.ylabel("Energy (GeV)")
pylab.xlim(-1,0)
pylab.ylim(6,56)
cbar.set_label("#Events Difference from PRD")
pylab.clim(-40,40)
pylab.savefig("KinDiffTh23P058Plot.png")
pylab.close()
