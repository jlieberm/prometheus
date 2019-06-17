

BASEPATH_EGAM1=cern_data/PhysVal/EGAM1/*
BASEPATH_EGAM7=cern_data/PhysVal/EGAM7/*

BASEPATH_EGAM1_BEFORE_TS1=cern_data/PhysVal/EGAM1/before_ts1/*

BASEPATH_EGAM1_BEFORE_TS1=cern_data/PhysVal/EGAM1/before_ts1/*
BASEPATH_EGAM1_AFTER_TS1=cern_data/PhysVal/EGAM1/after_ts1/*

BASEPATH_EGAM7_BEFORE_TS1=data_cern/EGAM7/before_ts1/*
BASEPATH_EGAM7_AFTER_TS1=data_cern/EGAM7/after_ts1/*


command_1="python job_collector.py --Zee"
#command_2="python job_collector.py --egam7"

prun_jobs.py -i $BASEPATH_EGAM1  -c $command_1 -mt 30
#prun_jobs.py -i $BASEPATH_EGAM7  -c $command_2 -mt 30











