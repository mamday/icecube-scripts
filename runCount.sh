#!/bin/sh

dir='/data/sim/IceCube/2012/filtered/GENIE-PPC/numu/1451/1451/'
for i in `ls $dir`; do
	python NCCount.py /net/user/mamday/icetray/data/GeometryFiles/GeoCalibDetectorStatus_IC86.55697_corrected_V2.i3 $dir$i
done 
