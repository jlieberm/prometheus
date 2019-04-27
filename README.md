[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/Naereen/)
[![pipeline status](https://gitlab.cern.ch/jodafons/prometheus/badges/master/pipeline.svg)](https://gitlab.cern.ch/jodafons/prometheus/commits/master)
## The Prometheus Analysis Framework



## The Gaugi core:


## The simulator:

## Requirements

- root (https://gitlab.cern.ch/jodafons/root.git)
- boost
- numpy
- python (2.7)


## Install the custom Root CERN package (Required)



## Before the installation

```
# dowload all submodules
source setup_module.sh
# put everything to master
source setup_module.sh --head
```



## Standalone Installation

```
# setup all standalone envs
source setup_standalone.sh
# build and compile
source buildthis.sh
# setup the libs and modules
source setup_prometheus
```

## Athena Installation

```
# setup all ATLAS envs
source setup_athena.sh
# build and compile
source buildthis.sh
# setup the libs and modules
source build/x86-*/setup.sh
```

