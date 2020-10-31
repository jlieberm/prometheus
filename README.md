
# Prometheus 

![](https://travis-ci.com/jodafons/prometheus.svg?branch=master)

In 2017 the ATLAS experiment implemented an ensemble of neural networks (NeuralRinger algorithm) dedicated to improving the performance of filtering events containing electrons in the high-input rate online environment of the Large Hadron Collider at CERN, Geneva. The ensemble employs a concept of calorimetry rings. The training procedure and final structure of the ensemble are used to minimize fluctuations from detector response, according to the particle energy and position of incidence. This reposiroty is dedicated to hold all analysis scripts for each subgroup in the ATLAS e/g trigger group.


## Requiriments:

- root;
- make
- gaugi

## Installation:

Use `make` to install this repository into your python path. 

```bash
mkdir build && cd build
cmake .. && make && cd ..
source setup.sh
```

## Struture:


