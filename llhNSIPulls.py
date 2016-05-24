#!/usr/bin/env python
import cPickle as pickle
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import glob
import sys,numpy,pylab
import math
file_list = glob.glob(sys.argv[1])

n_pull = []
ne_pull = []
g_pull = []
atm_pull = []
de_pull = []
hi_pull = []
llh_diff = []
exp_rat = []
exp1_rat = []
mt_list = []
mtp_list = []
ttdiff_list = []
ttpdiff_list = []
count=0
count1=0
for lfile in file_list:
  try:
    #llh_file = pickle.load(open("RandNPFogliEMTNull-"+lfile, "rb"))
    #llh_file = pickle.load(open("RandNoStats2NeutEMTNull-"+lfile, "rb"))
    llh_file = pickle.load(open("RandNormSystNP2NeutEMTNull-"+lfile, "rb"))
    #llh_file = pickle.load(open(lfile, "rb"))
    #llh_file1 = pickle.load(open("RandNPFogliFixEMTDM2Null-"+lfile, "rb"))
    #llh_file1 = pickle.load(open("RandNoStats2NeutFixEMTDM2Null-"+lfile, "rb"))
    llh_file1 = pickle.load(open("RandNormSystNP2NeutFixEMTDM2Null-"+lfile, "rb"))
#    print llh_file['result'] 
#    print llh_file1['result'] 
    mt = float("%.5f" % llh_file['result']['mt'])
    tt = float("%.5f" % llh_file['result']['tt'])
    th23 = float("%.5f" % llh_file['result']['theta23'])
    exp = float("%d" % llh_file['result']['expected_events'][0])
    mix = float("%.5f" % llh_file['result']['mix_angle'])
    dm2 = float("%.5f" % llh_file['result']['dm31'])
    mt1 = float("%.5f" % llh_file1['result']['mt'])
    tt1 = float("%.5f" % llh_file1['result']['tt'])
    th231 = float("%.5f" % llh_file1['result']['theta23'])
    exp1 = float("%d" % llh_file1['result']['expected_events'][0])
    mix1 = float("%.5f" % llh_file1['result']['mix_angle'])
    dm21 = float("%.5f" % llh_file1['result']['dm31'])
#    print mt,tt,float("%.5f" % llh_file1['result']['tt']),tt-float("%.5f" % llh_file1['result']['tt'])
    if(llh_file['result']['fit_stat']=='Suceeded' and llh_file1['result']['fit_stat']=='Suceeded'):
      exp_rat.append(exp/float(5174))
      exp1_rat.append(exp1/float(5174))
      count+=1
      if(dm2!=0.00165):
        count1+=1
      #if((mix)<1.0):
      if((th23)<0.785):
      #if((mt)<0.0):
      #if((1000*dm2)<3.0):
        mt_list.append(th23)
        #mt_list.append(mix)
        #mt_list.append(mt)
        #mt_list.append(1000*dm2)
        #ttdiff_list.append(mt-float("%.5f" % llh_file1['result']['mt']))
      else:
        mtp_list.append(th23)
        #mtp_list.append(mix)
        #mtp_list.append(mt)
        #mtp_list.append(1000*dm2)
        #ttpdiff_list.append(mt-float("%.5f" % llh_file1['result']['mt']))
      #if((mix1)<1.0):
      if((th231)<1.0):
        #ttdiff_list.append(mix1)
        ttdiff_list.append(th231)
      else:
        #ttpdiff_list.append(mix1)
        ttpdiff_list.append(th231)

#    if(2*(float("%.5f" % llh_file1['result']['llh'])-float("%.5f" % llh_file['result']['llh']))<0.05):
#      print mt,tt,float("%.5f" % llh_file1['result']['llh']),float("%.5f" % llh_file['result']['llh']),llh_file['result']['fit_stat']
#      print lfile 
#    if(llh_file1['result']['fit_stat']=='Suceeded'):
    if(llh_file['result']['fit_stat']=='Suceeded' and llh_file1['result']['fit_stat']=='Suceeded'):
    #  print mt,dm2,mt1,dm21
#      if(math.fabs(mt)>0.001):
        print dm2,th23,dm21,th231,2*(float("%.5f" % llh_file1['result']['llh'])-float("%.5f" % llh_file['result']['llh']))
        llh_diff.append(2*(float("%.5f" % llh_file1['result']['llh'])-float("%.5f" % llh_file['result']['llh'])))
    n_pull.append((float("%.5f" % llh_file['result']['norm'])-1)/0.5)
    ne_pull.append((float("%.5f" % llh_file['result']['norm_e'])-1)/1)
    g_pull.append((float("%.5f" % llh_file['result']['gamma'])-0)/5)
    atm_pull.append((float("%.5f" % llh_file['result']['atmmu_fraction'])-0.01)/1)
    de_pull.append((float("%.5f" % llh_file['result']['domeff'])-1)/0.3)
    hi_pull.append((float("%.5f" % llh_file['result']['hole_ice'])-0.02)/0.02)
  except:
    pass
    #print lfile
print len(llh_diff),len(n_pull)
from scipy import stats
print 'lists',count,count1,len(mt_list),len(mtp_list)
pylab.hist2d(mt_list+mtp_list,exp_rat,bins=20)
pylab.xlabel(r"Fitted $\theta_{23}$")
#pylab.xlabel(r"Fitted $sin^2(2 \theta_{23})$")
pylab.ylabel("Events/5174")
pylab.colorbar()
pylab.savefig("ElimPlot.pdf")
pylab.close()
pylab.hist2d(ttdiff_list+ttpdiff_list,exp1_rat,bins=20)
pylab.xlabel(r"Fitted $\theta_{23}$")
#pylab.xlabel(r"Fitted $sin^2(2 \theta_{23})$")
pylab.ylabel("Events/5174")
pylab.colorbar()
pylab.savefig("ElimPlot1.pdf")
pylab.close()
#pylab.hist(mt_list+mtp_list,bins=numpy.linspace(-0.01,0.01,30),color='k',histtype='step')
#pylab.hist(mt_list+mtp_list,bins=numpy.linspace(0.7,1.2,40),color='k',histtype='step')
#Normal non-zero plot
pylab.hist(mt_list+mtp_list,bins=numpy.linspace(0.5,1.0,50),color='k',histtype='step')
#pylab.hist(mt_list+mtp_list,bins=numpy.linspace(0.7,1.2,50),color='k',histtype='step')
#zero plot
#pylab.hist(mt_list+mtp_list,bins=numpy.linspace(0.0,3.14,30),color='k',histtype='step')
#pylab.hist(mt_list+mtp_list,bins=numpy.linspace(2,4,30),color='k',histtype='step')
#pylab.xlabel(r"1D Distribution of $\theta_{23}$")
#pylab.xlabel(r"1D Distribution of $\Delta_{m^2}$")
#pylab.xlim(-0.01,0.01)
#pylab.xlim(2,4)
#zero limits
#pylab.xlim(0.0,3.14)
#non-zero limits
#pylab.axvline(0.737,color='r')
#pylab.axvline(0.754,color='k')
#pylab.axvline(0.785,color='b')
pylab.xlim(0.5,1.0)
#pylab.xlim(0.7,1.2)
#pylab.xlim(2.0,4.0)
#pylab.xlim(-0.01,0.01)
pylab.ylim(0.0,100)
pylab.xlabel(r"Fitted $\theta_{23}$")
#pylab.xlabel(r"Fitted $sin^2(2 \theta_{23})$")
#pylab.xlabel(r"Fitted $\epsilon_{\mu \tau}$")
#pylab.xlabel(r"Fitted $\Delta_{m^2}$")
pylab.ylabel("Number of Events")
#pylab.ylim(0.0,100)
pylab.savefig("Th231DDist.pdf")
#pylab.savefig("EMTDist.pdf")
#pylab.savefig("DM2Dist.pdf")
pylab.close()
print 'Lalahaha'
#pslope,pintercept, pr_value, pp_value, pstd_err = stats.linregress(mtp_list,ttpdiff_list)
#slope,intercept, r_value, p_value, std_err = stats.linregress(mt_list,ttdiff_list)
#print 'Stats',pr_value,pp_value,r_value,p_value
#plt.plot(mt_list,slope*numpy.array(mt_list)+intercept,color='r')
#plt.plot(mt_list,[0 for i in mt_list],color='k')
#plt.plot(mtp_list,[0 for i in mtp_list],color='k')
#plt.plot(mtp_list,slope*numpy.array(mtp_list)+intercept,color='b')
#plt.plot(mtp_list,pslope*numpy.array(mtp_list)+pintercept,color='b')
#plt.scatter(mt_list+mtp_list,ttdiff_list+ttpdiff_list)
#pylab.xlabel(r"Fitted $\theta_{23}$") 
#pylab.ylabel(r"Fitted $\epsilon^{\mu \tau} Difference$") 
#pylab.savefig('MTVTT.pdf')
pylab.close()
dist = numpy.random.chisquare(2,100000) 
dist1 = numpy.random.chisquare(1,100000) 
pylab.hist(llh_diff,histtype='step',bins=numpy.linspace(-5,5,21),weights=(1/float(len(llh_diff)))*numpy.array([float(1) for i in llh_diff]),color='k',label='Ensemble Tests')
pylab.hist(dist1,histtype='step',bins=numpy.linspace(-5,5,21),weights=(1/float(100000))*numpy.array([float(1) for i in xrange(100000)]),color='b',label=r'$\chi^2 DOF=1$')
pylab.hist(dist,histtype='step',bins=numpy.linspace(-5,5,21),weights=(1/float(100000))*numpy.array([float(1) for i in xrange(100000)]),color='r',label=r'$\chi^2 DOF=2$')
#pylab.plot(numpy.linspace(0,5,len(llh_diff)),dist,color='r')
pylab.xlim(-5,5)
pylab.legend()
pylab.xlabel("Test Statistic Distribution (Inj-Fitted LLH)")
pylab.savefig("TestStatDist.pdf")
pylab.close()
#pylab.hist(n_pull,histtype='step',bins=numpy.linspace(-1.5,1.5,31),color='k')
#pylab.xlabel("Pull (Fit-Inj)/(Sigma)")
#pylab.savefig("PullsNorm.pdf")
#pylab.close()
pylab.hist(ne_pull,histtype='step',bins=numpy.linspace(-1.5,1.5,31),color='k')
pylab.xlabel("Pull (Fit-Inj)/(Sigma)")
pylab.savefig("PullsNormE.pdf")
pylab.close()
pylab.hist(g_pull,histtype='step',bins=numpy.linspace(-1.5,1.5,31),color='k')
pylab.xlabel("Pull (Fit-Inj)/(Sigma)")
pylab.savefig("PullsGamma.pdf")
pylab.close()
pylab.hist(hi_pull,histtype='step',bins=numpy.linspace(-1.5,1.5,31),color='k')
pylab.xlabel("Pull (Fit-Inj)/(Sigma)")
pylab.savefig("PullsHI.pdf")
pylab.close()
pylab.hist(de_pull,histtype='step',bins=numpy.linspace(-1.5,1.5,31),color='k')
pylab.xlabel("Pull (Fit-Inj)/(Sigma)")
pylab.savefig("PullsDE.pdf")
pylab.close()
pylab.hist(atm_pull,histtype='step',bins=numpy.linspace(-1.5,1.5,31),color='k')
pylab.xlabel("Pull (Fit-Inj)/(Sigma)")
pylab.savefig("PullsAtm.pdf")
pylab.close()
