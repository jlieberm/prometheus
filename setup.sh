export Athena_SETUP=off
export CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:/usr/include/python2.7/"
export LC_ALL=''
export RCM_NO_COLOR=0
export RCM_GRID_ENV=0
export CALIBPATH=/cvmfs/atlas.cern.ch/repo/sw/database/GroupData

export PATH=$PATH:$PWD/Gaugi/scripts



cd build
rm -rf lib
mkdir lib
for file in "`pwd`"/**/*.pcm
do
  echo "$file"
  ln -sf $file lib
done 

for file in "`pwd`"/**/*.so
do
  echo "$file"
  ln -sf $file lib
done 

export LD_LIBRARY_PATH=`pwd`/lib:$LD_LIBRARY_PATH
export PYTHONPATH=`pwd`/python:$PYTHONPATH
cd ..


export PATH=$PATH:`pwd`/Tools/EfficiencyTools/scripts





