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

cov = in_file['result']['covariance']

sys_list = []
cov_list = []
for key in cov.keys():
  print key,cov[key]
  if((key[0]==key[1]) and not(key[0] in sys_list)):
    sys_list.append(key[0])
    cov_list.append(math.sqrt(math.fabs(float(cov[key]))))
    if(float(cov[key])<0):
      print 'Neg',key,float(cov[key])
print cov,len(sys_list),len(cov_list),cov_list,sys_list

cov_arr = numpy.empty([len(cov_list),len(cov_list)])
count=-1
count1=-1
for ind,i in enumerate(sys_list):
  count+=1
  count1=-1
  for ind1,j in enumerate(sys_list):
    count1+=1
    print count,count1,i,j,cov[(i,j)],cov_list[ind],cov_list[ind1],i,j,math.fabs(cov[(i,j)]/(cov_list[ind]*cov_list[ind1]))
    cov_arr[count1][count] = (cov[(i,j)]/(cov_list[ind]*cov_list[ind1]))    
    #if((ind==ind1) and sys_list[ind]=='theta23'):
    #  print 'This totally happened',cov_arr[count1][count]
    #  cov_arr[count1][count]*=-1
    #  print 'This totally happened again',cov_arr[count1][count]
print cov_arr
cs = pylab.pcolormesh(numpy.array(range(len(sys_list)+1)),numpy.array(range(len(sys_list)+1)),cov_arr,cmap=cm.RdYlBu,vmin=-1.0,vmax=1.0)
plt.xticks(range(len(sys_list)),sys_list,size='small')
plt.yticks(range(len(sys_list)),sys_list,size='small')
plt.tick_params(labelsize=7)
cbar = plt.colorbar(cs)
cbar.set_clim(-1.0,1.0)
cbar.set_label("Correlation (Absolute value)")
pylab.savefig("CorrMat.png")
