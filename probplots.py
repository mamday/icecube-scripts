import numpy
import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import pylab

file_name = sys.argv[1]
file_name1 = sys.argv[2]
file_name2 = sys.argv[3]
file_name3 = sys.argv[4]
file_name4 = sys.argv[5]
file_name5 = sys.argv[6]
p_file = open(file_name)
p_file1 = open(file_name1)
p_file2 = open(file_name2)
p_file3 = open(file_name3)
p_file4 = open(file_name4)
p_file5 = open(file_name5)

prob_info = []
prob_info1 = []
prob_info2 = []
prob_info3 = []
prob_info4 = []
prob_info5 = []
for line in p_file.readlines():
  info = line.split(" ")
  prob_info.append((info[0],float(info[1]),float(info[2])))

for line in p_file1.readlines():
  info = line.split(" ")
  prob_info1.append((info[0],float(info[1]),float(info[2])))

for line in p_file2.readlines():
  info = line.split(",")
  prob_info2.append((float(info[0]),float(info[1])))

for line in p_file3.readlines():
  info = line.split(",")
  prob_info3.append((float(info[0]),float(info[1])))

for line in p_file4.readlines():
  info = line.split(",")
  prob_info4.append((float(info[0]),float(info[1])))

for line in p_file5.readlines():
  info = line.split(",")
  prob_info5.append((float(info[0]),float(info[1])))

print prob_info2,prob_info3
#matplotlib.pyplot.plot((numpy.array([j for i,j,k in prob_info if i=='Neutrino' and j>9])),0.7*numpy.array([k for i,j,k in prob_info if i=='Neutrino' and j>9])+0.3*numpy.array([k for i,j,k in prob_info if i=='Anti-Neutrino' and j>9]))
#matplotlib.pyplot.plot((numpy.array([j for i,j,k in prob_info1 if i=='Neutrino' and j>9])),0.7*numpy.array([k for i,j,k in prob_info1 if i=='Neutrino' and j>9])+0.3*numpy.array([k for i,j,k in prob_info1 if i=='Anti-Neutrino' and j>9]),color='r')
matplotlib.pyplot.plot((numpy.array([j for i,j,k in prob_info if i=='Neutrino' and j>9])),numpy.array([k for i,j,k in prob_info if i=='Neutrino' and j>9]))
matplotlib.pyplot.plot(numpy.array([i for i,j in prob_info2]),numpy.array([j for i,j in prob_info2]),color='midnightblue')
matplotlib.pyplot.plot((numpy.array([j for i,j,k in prob_info1 if i=='Neutrino' and j>9])),numpy.array([k for i,j,k in prob_info1 if i=='Neutrino' and j>9]),color='r')
matplotlib.pyplot.plot(numpy.array([i for i,j in prob_info3]),numpy.array([j for i,j in prob_info3]),color='darkred')
#pylab.xlabel("Energy (GeV)")
#pylab.xlim(1,3)
pylab.xlim(10,1000)
pylab.xlabel("Log(Energy) (GeV)")
pylab.xscale('log')
pylab.ylabel(r"$\nu_{\mu}$ Survival Probability")
pylab.savefig("NeutProbNoNSI.png") 
pylab.close()
matplotlib.pyplot.plot((numpy.array([j for i,j,k in prob_info if i=='Neutrino' and j>9])),numpy.array([k for i,j,k in prob_info if i=='Anti-Neutrino' and j>9]))
matplotlib.pyplot.plot(numpy.array([i for i,j in prob_info4]),numpy.array([j for i,j in prob_info4]),color='midnightblue')
matplotlib.pyplot.plot((numpy.array([j for i,j,k in prob_info1 if i=='Neutrino' and j>9])),numpy.array([k for i,j,k in prob_info1 if i=='Anti-Neutrino' and j>9]),color='r')
matplotlib.pyplot.plot(numpy.array([i for i,j in prob_info5]),numpy.array([j for i,j in prob_info5]),color='darkred')
pylab.xlim(10,1000)
pylab.xscale('log')
pylab.xlabel("Log(Energy) (GeV)")
pylab.ylabel(r"$\nu_{\mu}$ Survival Probability")
pylab.savefig("AntiNeutProbNoNSI.png") 
