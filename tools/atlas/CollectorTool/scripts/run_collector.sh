

BASEPATH_EGAM1=cern_data/PhysVal/EGAM1/*
BASEPATH_EGAM7=cern_data/PhysVal/EGAM7/*

BASEPATH_EGAM1_BEFORE_TS1=cern_data/PhysVal/EGAM1/before_ts1/*

BASEPATH_EGAM1_BEFORE_TS1=cern_data/PhysVal/EGAM1/before_ts1/*
BASEPATH_EGAM1_AFTER_TS1=cern_data/PhysVal/EGAM1/after_ts1/*

BASEPATH_EGAM7_BEFORE_TS1=data_cern/EGAM7/before_ts1/*
BASEPATH_EGAM7_AFTER_TS1=data_cern/EGAM7/after_ts1/*

# Jpsi data
BASEPATH_EGAM2_2017=/volume/Physval/data17_13TeV/EGAM2/user.*
BASEPATH_EGAM7_2017=/volume/Physval/data17_13TeV/EGAM7/user.*

BASEPATH_EGAM2_2017=/volume/Physval/data18_13TeV/EGAM2/user.*
BASEPATH_EGAM7_2018=/volume/Physval/data18_13TeV/EGAM7/user.*

command_1="python job_collector.py --Zee"
command_2="python job_collector.py --egam7"

# Jpsi command
command_3="python job_collector.py --Jpsi"
command_4="python job_collector.py --Jpsi --egam7"


# Joao
#prun_jobs.py -i $BASEPATH_EGAM7  -c 'python3 job_collector.py --egam7' -mt 30
#mkdir EGAM7
#mv output* EGAM7


prun_jobs.py -i $BASEPATH_EGAM1  -c 'python3 job_collector.py --Zee' -mt 30 --base_id 23401 --skip_to 280
mkdir EGAM1
mv output* EGAM1




#prun_jobs.py -i $BASEPATH_EGAM2_2018  -c 'python3 job_collector.py --Jpsi' -mt 30
#prun_jobs.py -i /volume/Physval/data17_13TeV/EGAM2/user.*  -c 'python3 job_collector.py --Jpsi' -mt 30
#mkdir EGAM2_17
#mv output* EGAM2_17
#prun_jobs.py -i $BASEPATH_EGAM7_2017  -c 'python3 job_collector.py --Jpsi --egam7' -mt 30
#mkdir EGAM7_17
#mv output* EGAM7_17









