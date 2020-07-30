#!/bin/bash

echo "======================================================================================"

echo "setup root..."
# Set ROOT by hand
export ROOTSYS="/opt/root/buildthis"
export PATH="$ROOTSYS/bin:$PATH"
export LD_LIBRARY_PATH="$ROOTSYS/lib:$LD_LIBRARY_PATH"
export PYTHONPATH="/opt/root/buildthis/lib:$PYTHONPATH"




echo "setup prometheus..."
cd $HOME
ls -lisah
git clone https://github.com/jodafons/prometheus.git
cd prometheus
ls -lisah
mkdir build && cd build && cmake .. && make

for file in "`pwd`"/*/*.pcm
do
  echo "ln -sf $file lib"
  ln -sf $file lib
done 

for file in "`pwd`"/*.so
do
  echo "ln -sf $file lib"
  ln -sf $file lib
done 



export LC_ALL=''
export RCM_NO_COLOR=0
export RCM_GRID_ENV=0
export CALIBPATH=/cvmfs/atlas.cern.ch/repo/sw/database/GroupData
export LD_LIBRARY_PATH=`pwd`/lib:$LD_LIBRARY_PATH
export PYTHONPATH=`pwd`/python:$PYTHONPATH
cd ..
export PATH=`pwd`/tools/EfficiencyTools/scripts:$PATH

cd ..

echo "======================================================================================"
