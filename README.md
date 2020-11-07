
# Prometheus 

In 2017 the ATLAS experiment implemented an ensemble of neural networks (NeuralRinger algorithm) dedicated to improving the performance of filtering events containing electrons in the high-input rate online environment of the Large Hadron Collider at CERN, Geneva. The ensemble employs a concept of calorimetry rings. The training procedure and final structure of the ensemble are used to minimize fluctuations from detector response, according to the particle energy and position of incidence. This reposiroty is dedicated to hold all analysis scripts for each subgroup in the ATLAS e/g trigger group.


## How to run on singularity:

Download the prometheus local image to your home:
```bash
singularity pull docker://jodafons/prometheus:local
```

After donwload it, just execute the `run` command:
```bash
singularity run prometheus_local.sif
```

Inside of the singularity enviroment, just setup all prometheus dependencies using:
```bash
source /setup_here.sh
```

After that, you can download the prometheus repository into your home:

```bash
git clone https://github.com/jodafons/prometheus.git
```
and install it:
```bash
cd prometheus && mkdir build && cd build && cmake .. && make && cd ..
source setup.sh
```



## Framework status:

This table shows the branch status.

|  Branch    | Build Status |
| ---------- | ------------ |
|   Master   |[![Build Status](https://travis-ci.com/jodafons/prometheus.svg?branch=master)](https://travisci.org/jodafons/lorenzetti)  |

