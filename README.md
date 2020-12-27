# prometheus 

We should include some description here.

**NOTE**: This repository make part of the ringer analysis kit (rak).

## Organization:

We should include some description here.

## How to run on singularity:

Download the prometheus local image to your home:
```bash
singularity pull docker://jodafons/prometheus:base
```

After donwload it, just execute the `run` command:
```bash
singularity run prometheus_base.sif
```
**NOTE**: Use `--nv` after `run` argument to attach the gpu into the container if you have it.

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

|  Branch    | Build Status |
| ---------- | ------------ |
|   Master   | [![Build Status](https://travis-ci.com/jodafons/prometheus.svg?branch=master)](https://travisci.org/jodafons/lorenzetti) |


## Notes:


