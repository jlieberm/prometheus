
## The Prometheus Analysis Framework


## Requirements

- root (https://gitlab.cern.ch/jodafons/root.git)
- boost
- numpy
- python 3
- cmake 3
- geant 4 (https://github.com/jodafons/geant4_10.5.git)



## Install the custom Root CERN package (Required)

The ROOT system provides a set of OO frameworks with all the functionality
needed to handle and analyze large amounts of data in a very efficient way.
Having the data defined as a set of objects, specialized storage methods are
used to get direct access to the separate attributes of the selected objects,
without having to touch the bulk of the data. Included are histograming
methods in an arbitrary number of dimensions, curve fitting, function
evaluation, minimization, graphics and visualization classes to allow
the easy setup of an analysis system that can query and process the data
interactively or in batch mode, as well as a general parallel processing
framework, PROOF, that can considerably speed up an analysis.

Use apt-get (or yum) to install other dependencies (steps marked with recommended are not obligatory):

```bash
# Install gcc and other developer tools
sudo apt-get install coreutils
# Install python
sudo apt-get install python
# Install needed CVS
sudo apt-get install git subversion
# (Recommended) Install numpy and scipy
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
# (Recommended) Install boost
sudo apt-get install libboost-all-dev
```

And install the root package in your local directory:


```bash
# in your root dir
mkdir .bin
cd .bin
# download the root
git clone https://gitlab.cern.ch/jodafons/root.git
# checkout the custom branch
git checkout v6-16-00
# create the build dir
mkdir build
cd build
# For linux
cmake --Dpython_version=3   
# For MacOS
#cmake -DPYTHON_EXECUTABLE=/usr/local/bin/python3 \
#DPYTHON_INCLUDE_DIR=/usr/local/Cellar/python/3.7.2_1/Frameworks/Python.framework/Versions/3.7/Headers \
#-DPYTHON_LIBRARY=/usr/local/Cellar/python/3.7.2_1/Frameworks/Python.framework/Versions/3.7/lib/libpython3.7.dylib 
# and compile
make -j4
```

Then use this commands to include the root into your path.

```bash
echo 'source ~/.bin/root/build/bin/thisroot.sh' >> ~/.bashrc
source $HOME/root/bin/thisroot.sh
```




## Install the Geant 4 on your local machine (Required for simulation purpose)

```bash
mkdir .bin
cd .bin
git clone https://github.com/jodafons/geant4_10.5.git
cd geant4
source buildthis.sh
echo 'source ~/.bin/geant4/build/geant4.sh' >> ~/.bashrc
```



## Install prometheus Framework


```bash
# download from git
git clone https://github.com/jodafons/prometheus.git
# dowload all submodules
source setup_module.sh
# put everything to master
source setup_module.sh --head
# build and compile
source buildthis.sh
# setup the libs and modules
source setup.sh
```

If you shutdonw and must reset the prometheus once again, just apply:
```bash
# setup the libs and modules
source setup.sh
```



## Or set the Docker container (prometheus)

The locally volume is provide by a docker plugin. You must create your volume first. After setup your volume,
just tip the follow command:

```bash
docker run --network host -v my_volume_name:/volume -it jodafons/prometheus /bin/bash
```

and inside of the container:

```bash
source /setup_envs.sh
```

You can see the docker specification of this container here: https://github.com/jodafons/docker

### Docker volume locally (only for linux)

See this page: https://github.com/surgeforward/docker-local-persist-volume-plugin



## To run the simulator (Lorenzett)

You must have Geant4 installed in you machine. To run the simulator example:

```bash
cd Analysis/Simulator/calo_resolution
generator -m geant4_config.mac
# OR in parallel (30 threads, 100 jobs)
python3 run_generator.py
```

After generate the raw date, just run the reconstruction and analysis step

```bash
python3 job_resolution.py
```


## Contribution

- Dr. João Victor da Fonseca Pinto, UFRJ/COPPE, CERN/ATLAS (jodafons@cern.ch) [maintainer, developer]
- Dr. Werner Freund, UFRJ/COPPE, CERN/ATLAS (wsfreund@cern.ch) [developer]
- Msc. Micael Veríssimo de Araújo, UFRJ/COPPE, CERN/ATLAS (mverissi@cern.ch) [developer]


