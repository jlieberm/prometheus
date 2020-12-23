#!/bin/bash

current=$PWD
# setup root to be sure...
source /setup_envs.sh
cd $(mktemp -d)
temp=$PWD

git clone https://github.com/ringer-atlas/prometheus.git

echo "======================================================================================"
echo "setup prometheus..."
cd $temp/prometheus && mkdir build && cd build && cmake .. && make -j4 && cd ../ && source setup.sh
echo "======================================================================================"
echo "All repositories can be found at: $temp."
echo "======================================================================================"

cd $temp



