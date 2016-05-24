#!/usr/bin/env python
import cPickle as pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.path import Path
import glob
import sys,numpy,math,pylab
from scipy import *
from scipy import interpolate
from scipy.interpolate import interp1d 

file_list = glob.glob(sys.argv[1])
llh_dict = {}
min_dict = {}
fc_dict = {}
prof_dict = {}
prof_dict1 = {}
llh_diff = 0
mt_dict = {}
t_mts = []
max_run=-1
mt_val = float(sys.argv[2])
wilk_file = pickle.load(open(sys.argv[3],'rb'))
wilk_file1 = pickle.load(open(sys.argv[4],'rb'))
for lfile in file_list:
  try:
    fc_file = 'BrazilNull-'+lfile
    print fc_file,lfile 
    run = lfile[lfile.find('Brazil-')+7:]
    new_run=''
#Find the full integer since I stupidly did not make this a uniform length
    for c in run: 
      if c.isdigit():
        new_run+=c
      if(c=='-'):
        break
    run = int(new_run)
    len_run = len(new_run)
    if(run>max_run):
      max_run=run
#Find the value of e_mutau
    t_mt = float(lfile[lfile.find(new_run+'-')+len_run+1:lfile.find('.pckl')])
    if(not(t_mt in t_mts)):
      t_mts.append(t_mt)
    llh_file = pickle.load(open(lfile, "rb"))
    llh_file1 = pickle.load(open(fc_file, "rb"))
    prof_dict[(t_mt,run)] = llh_file['result']['profile']
    prof_dict1[(t_mt,run)] = llh_file1['result']['profile']
    llh_diff = llh_file1['result']['llh']-llh_file['result']['llh']
    #print 'Succeed',llh_file1['result'].keys()
    mt_dict[(t_mt,run)] = llh_file['result']['mt']
#    llh_spline = interp1d(prof_dict[(t_mt,run)][0],2*prof_dict[(t_mt,run)][1])
    close_mt = min(prof_dict[(t_mt,run)][0],key=lambda mt: abs(t_mt-mt))
    cur_ind = prof_dict[(t_mt,run)][0].index(close_mt)
    #print t_mt,close_mt,cur_ind
    if(t_mt in fc_dict):
      #fc_dict[t_mt].append(2*prof_dict[(t_mt,run)][1][cur_ind])
      fc_dict[t_mt].append(2*llh_diff)
    else:
      fc_dict[t_mt]=[]
      fc_dict[t_mt].append(2*llh_diff)
      #fc_dict[t_mt].append(2*prof_dict[(t_mt,run)][1][cur_ind])
    #print t_mt,llh_diff,fc_dict[t_mt]  
    #print 'Test Spline',llh_spline(t_mt)
    if(mt_val==t_mt):
      min_dict[run] = prof_dict[(t_mt,run)][0][prof_dict[(t_mt,run)][1].index(min(prof_dict[(t_mt,run)][1]))]
      for ind,i in enumerate(list(prof_dict[(t_mt,run)][0])):
        #print ind,i,prof_dict[(t_mt,run)][0][ind],prof_dict[(t_mt,run)][1][ind]
        if(i in llh_dict):
          llh_dict[i].append(2*prof_dict[(t_mt,run)][1][ind]) 
        else:
          llh_dict[i]=[]
          llh_dict[i].append(2*prof_dict[(t_mt,run)][1][ind]) 
    #print lfile,prof_dict[(t_mt,run)]
    #if(math.fabs(math.fabs(float(mt_dict[(t_mt,run)]))-math.fabs(float(t_mt)))>0.01):
    #  print mt_dict[(t_mt,run)],t_mt,math.fabs(float(mt_dict[(t_mt,run)]))-math.fabs(float(t_mt)),run
  except:
    pass
    #print lfile
mt_bounds = prof_dict[(mt_val,1)][0]
sepu_list = len(mt_bounds)*[0]
sepb_list = len(mt_bounds)*[0]
npu_list = len(mt_bounds)*[0]
npb_list = len(mt_bounds)*[0]
med_list = len(mt_bounds)*[0]
mean_list = len(mt_bounds)*[0]
for key,val in llh_dict.iteritems():
  ind = mt_bounds.index(key)
  sepu_list[ind] = numpy.percentile(val,84)
  sepb_list[ind] = numpy.percentile(val,16)
  npu_list[ind] = numpy.percentile(val,95)
  npb_list[ind] = numpy.percentile(val,5)
  med_list[ind] = numpy.percentile(val,50)
  mean_list[ind] = sum(val)/len(val)
mean_min = mt_bounds[mean_list.index(min(mean_list))]
for key,mins in min_dict.iteritems():
  if(mins==mean_min):
    mean_samp = prof_dict[(mt_val,key)][1]
    break
  #print 'Fin',ind,len(val),mt_bounds,numpy.percentile(val,68),numpy.percentile(val,90)
wilk_dist = wilk_file['result']['profile']
wilk_dist1 = wilk_file1['result']['profile']

pylab.plot(wilk_dist[0],wilk_dist[1],color='r',label=r'$\theta_{23}=0.74$')
pylab.plot(wilk_dist1[0],wilk_dist1[1],color='b',label=r'$\theta_{23}=0.67$')
pylab.plot(wilk_dist1[0],mean_samp,color='k',label=r'Sample $\theta_{23}=0.816$')
pylab.axhline(y=1.,color='k')
pylab.axhline(y=4.,color='k')
pylab.axhline(y=9.,color='k')
pylab.axhline(y=16.,color='k')
pylab.xlim(-0.012,0.012)
pylab.ylim(0,24)
pylab.xlabel(r'$\epsilon_{\mu \tau}$')
pylab.ylabel(r'$-2*\Delta LLH$')
pylab.grid()
pylab.legend(loc=1)
#pylab.savefig('BrazPThetas-%.4f.png' % (mt_val))
pylab.close()
#fig=plt.figure()
#verts = [
#    (0.011, 0.0), # left, bottom
#    (0.011, 1.0), # left, top
#    (-0.011, 1.0), # right, top
#    (-0.011, 0.0), # right, bottom
#    (0., 0.), # ignored
#    ]
#codes = [Path.MOVETO,
#         Path.LINETO,
#         Path.LINETO,
#         Path.LINETO,
#         Path.CLOSEPOLY,]
#path = Path(verts, codes)
#ax1 = fig.add_axes([0.1, 0.2, 0.8, 0.7])
#ax1.plot(wilk_dist1[0],med_list,color='k',label='Median')
#ax1.fill_between(mt_bounds,npb_list,npu_list,color=(255./255., 255./255., 11./255.),label='90%')
#ax1.fill_between(mt_bounds,sepb_list,sepu_list,color=(34./255., 255./255., 8./255.),label='68%')
#ax1.xaxis.grid()
#ax1.yaxis.grid()
#ax1.set_ylabel(r'$-2*\Delta LLH$')
#ax1.set_xlim(-0.012,0.012)
#ax1.set_ylim(0,24)
#ax1.fill(numpy.NaN, numpy.NaN,
#         facecolor=(255./255., 255./255., 11./255.),
#         alpha = 0.5,
#         label = "90% Range")
#ax1.fill(numpy.NaN, numpy.NaN,
#         facecolor=(34./255., 255./255., 8./255.),
#         alpha = 0.5,
#         label = "68% Range")
#ax1.axhline(y=1.,color='k')
#ax1.axhline(y=4.,color='k')
#ax1.axhline(y=9.,color='k')
#ax1.axhline(y=16.,color='k')
#ax1.legend(loc=1)
#ax2 = fig.add_axes([0.1, 0.1, 0.8, .05])
#patch = patches.PathPatch(path, facecolor='lightblue', lw=2)
#ax2.add_patch(patch)
#ax2.text(-0.005,0.2,'SuperK 90% Limits (arXiv:1109.1889)')
#ax2.set_xlim(-0.012,0.012)
#ax2.set_ylim(0,1)
#ax2.set_xlabel(r'$\epsilon_{\mu \tau}$')
#for label in ax2.get_yticklabels():
#	label.set_visible(False)
#for label in ax2.get_xticklabels():
#	label.set_visible(False)
#pylab.savefig('BrazPlot-%.4f.png' % (mt_val))
fc_1sig = len(t_mts)*[0]
fc_2sig = len(t_mts)*[0]
fc_90 = len(t_mts)*[0]
t_mts.sort()
for key,val in fc_dict.iteritems():
    ind = t_mts.index(key) 
#  if((numpy.percentile(val,68.3)-1)<0.1):
    fc_1sig[ind]=numpy.percentile(val,68.3)
#  if(((numpy.percentile(val,90)-2.7)/2.7)<0.1):
    fc_90[ind]=numpy.percentile(val,90)
#  if(((numpy.percentile(val,95.45)-4)/4)<0.1):
    fc_2sig[ind]=numpy.percentile(val,95)

  #print key,len(val),numpy.percentile(val,68.3)-1,(numpy.percentile(val,90)-2.71)/2.71,(numpy.percentile(val,95.45)-4)/2.71
  #print '1','2.71','3.84'
print t_mts,fc_1sig,fc_90,fc_2sig
pylab.plot(t_mts,fc_1sig,color='r') 
pylab.plot(t_mts,fc_90,color='r') 
pylab.plot(t_mts,fc_2sig,color='r')
pylab.axhline(y=1.,color='k')
pylab.axhline(y=2.71,color='k')
pylab.axhline(y=4.,color='k')
pylab.grid()
pylab.xlabel(r'$\epsilon_{\mu \tau}$')
pylab.ylabel(r'$-2*\Delta LLH$')
pylab.ylim(0,8)
pylab.xlim(-0.01,0.01)
pylab.savefig('FCPlots.png') 
