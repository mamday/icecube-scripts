import sys,os
import matplotlib
matplotlib.use('pdf')
import numpy,pylab
import cPickle as pickle
import glob
import math
file_list = glob.glob(sys.argv[1])

t_th23_list = []
t_dm2_list = []
th23_list = []
dm2_list = []
for lfile in file_list:
  try:
    in_file = pickle.load(open(lfile, "rb"))
    #t_th23 = float(lfile[11:16])
    #t_th23 = float(lfile[13:18])
    #t_th23 = float(lfile[20:25])
    #t_th23 = float(lfile[15:20])
    t_th23 = float(lfile[17:22])
    if(t_th23<0.405 or t_th23>1.195):
      continue
    t_dm2_list.append(float(lfile[23:30])) 
    #t_dm2_list.append(float(lfile[21:28])) 
    #t_dm2_list.append(float(lfile[19:26])) 
    #t_dm2_list.append(float(lfile[17:24])) 
    #t_dm2_list.append(float(lfile[26:33])) 

    th23 = float("%.3f" % in_file['result']['theta23'])
#    t_th23_list.append(numpy.sin(2*t_th23)**2)
    t_th23_list.append(t_th23)
#    th23_list.append(numpy.sin(2*th23)**2)
    if(numpy.sign(t_th23-0.785) != numpy.sign(th23-0.785)):
      if(th23>0.785):
        if(th23>=(2.355)):
          th23_list.append(0.785-(th23-2.355))
          print 'Ov1',t_th23,th23,th23_list[-1]
        elif(th23>=(1.57)):
          th23_list.append(0.785-(2.355-th23))
          print 'Ov2',t_th23,th23,th23_list[-1]
        else:
          th23_list.append(0.785-(th23-0.785))
          print 'Ov3',t_th23,th23,th23_list[-1]
      else:
        if(th23>=0.393):
          th23_list.append((0.785-th23)+0.785)
          print 'Und0',t_th23,th23,th23_list[-1]
        else:
          th23_list.append((0.393-th23)+0.785)
          print 'Und1',t_th23,th23,th23_list[-1]
    else:
      if((th23>=0.393 and th23<1.57)):
        th23_list.append(th23)
        print 'No0',t_th23,th23,th23_list[-1]
      elif(th23<0.393):
        th23_list.append(0.785-(0.393-th23))
        print 'No1',t_th23,th23,th23_list[-1]
      elif((th23>(1.57) and th23<=2.355)):
        th23_list.append(0.785+(2.355-th23))
        print 'No2',t_th23,th23,th23_list[-1]
      else:
        th23_list.append(0.785+(th23-2.355))
        print 'No3',t_th23,th23,th23_list[-1]
    if(th23_list[-1]<0.3):
      print 'Here'
    dm2_list.append(float("%.5f" % in_file['result']['dm31']))
    print 'DM2',t_dm2_list[-1],dm2_list[-1]
    #print numpy.sin(th23)**2,numpy.sin(t_th23)**2,dm2_list[-1],t_dm2_list[-1]
  except:
    print lfile

print len(t_th23_list),len(t_dm2_list),len(th23_list),len(dm2_list)
pylab.scatter(th23_list,dm2_list,color='r',marker='x')
pylab.scatter(t_th23_list,t_dm2_list,color='b',marker='x')
pylab.xlim(0.35,1.25)
pylab.xlabel(r'$\theta_{23}$')
pylab.ylim(0.0018,0.0042)
pylab.ylabel(r'$\Delta m^2_{32}$')
pylab.savefig('MySuchAs.png')

