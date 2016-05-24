import sys,os
import matplotlib
matplotlib.use('Agg')
import numpy,pylab
import cPickle as pickle
import glob
import math
file_list = glob.glob(sys.argv[1])

t_th23_list = []
t_dm2_list = []
t_emt_list = []
th23_list = []
dm2_list = []
emt_list = []
dmprof_list = []
for lfile in file_list:
  try:
    in_file = pickle.load(open(lfile, "rb"))
    first_num = lfile.find('-')
    #if(lfile[first_num+1]=='-'):
    sec_num = lfile[first_num+2:].find('-')
    t_emt = float(lfile[first_num+1:first_num+sec_num+2])
    third_num = lfile[first_num+sec_num+3:].find('-')
    t_dm2 = float(lfile[first_num+sec_num+3:first_num+sec_num+third_num+3])
    fourth_num = lfile[first_num+sec_num+4+third_num:].find('.p')
    t_th23=float(lfile[first_num+sec_num+third_num+4:first_num+sec_num+third_num+4+fourth_num])
    #print t_emt,t_dm2,t_th23,lfile
    if(t_th23<0.39 or t_th23>1.205):
      continue
    if(t_dm2>0.0039 or t_dm2<0.0029):
      continue
    print 'Succeed',lfile
    t_dm2_list.append(t_dm2) 
    dmprof = in_file['result']['dmprofile'] 
    dmprof_list.append(dmprof)
    th23 = float("%.3f" % in_file['result']['theta23'])
    emt = float("%.3f" % in_file['result']['mt'])
    t_emt_list.append(t_emt)
    emt_list.append(emt)
    t_th23_list.append(t_th23)
    if(numpy.sign(t_th23-0.785) != numpy.sign(th23-0.785)):
      if(th23>0.785):
        if(th23>=(2.355)):
          th23_list.append(0.785-(th23-2.355))
          #print 'Ov1',t_th23,th23,th23_list[-1]
        elif(th23>=(1.57)):
          th23_list.append(0.785-(2.355-th23))
          #print 'Ov2',t_th23,th23,th23_list[-1]
        else:
          th23_list.append(0.785-(th23-0.785))
          #print 'Ov3',t_th23,th23,th23_list[-1]
      else:
        if(th23>=0.393):
          th23_list.append((0.785-th23)+0.785)
          #print 'Und0',t_th23,th23,th23_list[-1]
        else:
          th23_list.append((0.393-th23)+0.785)
          #print 'Und1',t_th23,th23,th23_list[-1]
    else:
      if((th23>=0.393 and th23<1.57)):
        th23_list.append(th23)
        #print 'No0',t_th23,th23,th23_list[-1]
      elif(th23<0.393):
        th23_list.append(0.785-(0.393-th23))
        #print 'No1',t_th23,th23,th23_list[-1]
      elif((th23>(1.57) and th23<=2.355)):
        th23_list.append(0.785+(2.355-th23))
        #print 'No2',t_th23,th23,th23_list[-1]
      else:
        th23_list.append(0.785+(th23-2.355))
        #print 'No3',t_th23,th23,th23_list[-1]
    #if(th23_list[-1]<0.3):
      #print 'Here'
    dm2_list.append(float("%.5f" % in_file['result']['dm31']))
    #print t_emt-float(emt),lfile
    #print t_emt-float(emt),t_dm2-float(dm2),t_th23-float(th23),lfile
  except:
    print lfile
t_emt_list = numpy.array(t_emt_list)
t_th23_list = numpy.array(t_th23_list)
emt_list = numpy.array(emt_list)
th23_list = numpy.array(th23_list)
dm2_list = numpy.array(dm2_list)
dmprof_list = numpy.array(dmprof_list)

print dm2_list[t_emt_list==-0.007],dmprof_list[(t_emt_list==-0.007)][0],t_th23_list[t_emt_list==-0.007],emt_list[t_emt_list==-0.007],t_emt_list[t_emt_list==-0.007],len(th23_list),len(dm2_list),len(emt_list)
pylab.plot(dmprof_list[(t_emt_list==-0.007) & (t_th23_list==0.95)][0][0],2*dmprof_list[(t_emt_list==-0.007) & (t_th23_list==0.95)][0][1],color='k')
pylab.xlabel(r'$\Delta m^2_{23}$')
pylab.ylabel(r'2*$\Delta$ LLH')
pylab.savefig("DM2Profile-%f-%f.png" % (-0.007,0.95))
pylab.close()

#print len(t_th23_list),len(t_dm2_list),len(th23_list),len(dm2_list)
#pylab.xlabel(r'Fitted $\epsilon_{\mu \tau}$')
#pylab.ylabel(r'True $\epsilon_{\mu \tau}$')
#pylab.savefig('MySuchNSIAs-0.65.png')
pylab.scatter(t_emt_list[t_th23_list==0.65],emt_list[t_th23_list==0.65],color='b',marker='o',s=40,alpha=0.5,label=r'$\theta_{23}$=37$\degree$')
pylab.scatter(t_emt_list[t_th23_list==0.95],emt_list[t_th23_list==0.95],color='r',marker='+',s=40,alpha=0.5,label=r'$\theta_{23}$=54$\degree$')
#pylab.xlabel(r'Fitted $\epsilon_{\mu \tau}$')
#pylab.ylabel(r'True $\epsilon_{\mu \tau}$')
#pylab.savefig('MySuchNSIAs-0.95.png')
#pylab.close()
pylab.scatter(t_emt_list[t_th23_list==0.8],emt_list[t_th23_list==0.8],color='k',marker='x',s=40,alpha=0.5,label=r'$\theta_{23}$=46$\degree$')
pylab.ylabel(r'Fitted $\epsilon_{\mu \tau}$')
pylab.xlabel(r'True $\epsilon_{\mu \tau}$')
#pylab.savefig('MySuchNSIAs-0.8.png')
pylab.legend(loc=2)
pylab.grid()
pylab.savefig('MySuchNSIAs.png')
pylab.close()
pylab.scatter(t_emt_list[t_th23_list==0.65],th23_list[t_th23_list==0.65],color='b',marker='o',s=40,alpha=0.5,label=r'$\theta_{23}$=37$\degree$')
pylab.scatter(t_emt_list[t_th23_list==0.95],th23_list[t_th23_list==0.95],color='r',marker='+',s=40,alpha=0.5,label=r'$\theta_{23}$=54$\degree$')
pylab.scatter(t_emt_list[t_th23_list==0.8],th23_list[t_th23_list==0.8],color='k',marker='x',s=40,alpha=0.5,label=r'$\theta_{23}$=46$\degree$')
pylab.ylabel(r'Fitted $\theta_{23}$')
pylab.xlabel(r'True $\epsilon_{\mu \tau}$')
#pylab.legend(loc=2)
pylab.grid()
pylab.savefig('MySuchTh23NSIAs.png')
pylab.close()
pylab.scatter(t_emt_list[t_th23_list==0.65],dm2_list[t_th23_list==0.65],color='b',marker='o',s=40,alpha=0.5,label=r'$\theta_{23}$=37$\degree$')
pylab.scatter(t_emt_list[t_th23_list==0.95],dm2_list[t_th23_list==0.95],color='r',marker='+',s=40,alpha=0.5,label=r'$\theta_{23}$=54$\degree$')
pylab.scatter(t_emt_list[t_th23_list==0.8],dm2_list[t_th23_list==0.8],color='k',marker='x',s=40,alpha=0.5,label=r'$\theta_{23}$=46$\degree$')
pylab.ylabel(r'Fitted $\Delta m^2_{23}$')
pylab.xlabel(r'True $\epsilon_{\mu \tau}$')
pylab.legend(loc=2)
pylab.grid()
pylab.savefig('MySuchDM2NSIAs.png')
pylab.close()
#pylab.scatter(t_emt_list,emt_list,color='k',marker='x')
#print t_emt_list,t_th23_list,t_emt_list[(t_th23_list<0.9) & (t_th23_list>0.7)],t_emt_list[t_th23_list==0.95]
#pylab.scatter(t_th23_list,t_dm2_list,color='b',marker='x')
#pylab.xlim(0.35,1.25)
#pylab.ylim(0.0018,0.0042)
#pylab.ylabel(r'$\Delta m^2_{32}$')

