#!/bin/bash

BASEPATH_EGAM2=/home/micael/Documents/NeuralRinger/physvall_data/data17_13TeV/EGAM2/user.*
BASEPATH_EGAM7=/home/micael/Documents/NeuralRinger/physvall_data/data17_13TeV/EGAM7/user.*

command_1="\"python3 job_correction_v1_data17_13TeV_EGAM2_probes_lhmedium_EGAM7_vetolhvloose.py --Jpsiee\""
command_2="\"python3 job_correction_v1_data17_13TeV_EGAM2_probes_lhmedium_EGAM7_vetolhvloose.py --Jpsiee --egam7 \""


# run over signal
prun_jobs.py -i $BASEPATH_EGAM2 \
                -c "python3 job_correction_v1_data17_13TeV_EGAM2_probes_lhmedium_EGAM7_vetolhvloose.py --Jpsiee" \
                -mt 6
mkdir EGAM2
prun_merge.py -i output_* -o egam2.root -nm 35 -mt 6
mv *.root EGAM2

# run over background
prun_jobs.py -i $BASEPATH_EGAM7 \
                -c "python3 job_correction_v1_data17_13TeV_EGAM2_probes_lhmedium_EGAM7_vetolhvloose.py --Jpsiee --egam7" \
                -mt 6
mkdir EGAM7
prun_merge.py -i output_* -o egam7.root -nm 35 -mt 6
mv *.root EGAM7