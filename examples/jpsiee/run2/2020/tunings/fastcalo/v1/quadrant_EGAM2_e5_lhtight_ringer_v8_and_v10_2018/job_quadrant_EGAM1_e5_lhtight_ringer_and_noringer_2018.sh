

BASEPATH_EGAM1_2018=/data/jodafons/cern_data/data18_13TeV/PhysVal_v2/EGAM2

command_1="python job_quadrant_EGAM1_e5_lhtight_ringer_and_noringer_2018.py --Jpsiee"

prun_jobs.py -i $BASEPATH_EGAM1_2018  -c $command_1 -mt 50








