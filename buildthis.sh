
#source setup_module.sh
#source setup_module.sh --head
export G4_SETUP=on
export Athena_SETUP=off

mkdir build
cd build
cmake3 ..
make -j4
cd ..


