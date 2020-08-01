#!/bin/bash

echo "======================================================================================"

current_dir=$PWD


echo "setup root..."
# Set ROOT by hand
export ROOTSYS="/opt/root/buildthis"
export PATH="$ROOTSYS/bin:$PATH"
export LD_LIBRARY_PATH="$ROOTSYS/lib:$LD_LIBRARY_PATH"
export PYTHONPATH="/opt/root/buildthis/lib:$PYTHONPATH"


echo "setup prometheus..."
cd /code/prometheus
git pull
export PYTHONPATH=`pwd`/build/python:$PYTHONPATH
export PATH=`pwd`/tools/analysis/EfficiencyTools/scripts:$PATH
export PRT_PATH=`pwd`
cd $current_dir

echo "======================================================================================"
