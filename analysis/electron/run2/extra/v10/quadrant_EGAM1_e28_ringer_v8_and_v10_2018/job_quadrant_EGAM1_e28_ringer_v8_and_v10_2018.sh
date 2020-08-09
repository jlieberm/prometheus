

BASEPATH_EGAM1_2018=/data/jodafons/cern_data/data18_13TeV/PhysVal_v2/EGAM1
BASEPATH_EGAM7_2018=/data/jodafons/cern_data/data18_13TeV/PhysVal_v2/EGAM7

command_1="python job_quadrant.py --Zee"

prun_jobs.py -i $BASEPATH_EGAM1_2018  -c $command_1 -mt 50

#mkdir egam1_after_ts1
#prun_merge.py -i output_* -o egam1.root -nm 50 -mt 30
#mv *.root egam1_after_ts1










