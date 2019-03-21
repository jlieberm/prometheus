



BASEPATH_EGAM1_BEFORE_TS1=data_cern/EGAM1/before_ts1/*
BASEPATH_EGAM1_AFTER_TS1=data_cern/EGAM1/after_ts1/*
BASEPATH_EGAM7_BEFORE_TS1=data_cern/EGAM7/before_ts1/*
BASEPATH_EGAM7_AFTER_TS1=data_cern/EGAM7/after_ts1/*


command_1="python job_quadrant.py --Zee"

prun_jobs.py -i $BASEPATH_EGAM1_AFTER_TS1  -c $command_1 -mt 30

#mkdir egam1_after_ts1
#prun_merge.py -i output_* -o egam1.root -nm 50 -mt 30
#mv *.root egam1_after_ts1










