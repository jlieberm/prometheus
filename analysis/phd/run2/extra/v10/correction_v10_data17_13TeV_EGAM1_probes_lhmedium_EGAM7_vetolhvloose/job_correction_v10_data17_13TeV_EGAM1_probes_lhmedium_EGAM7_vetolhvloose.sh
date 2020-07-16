


command_1='python job_correction_v10_data17_13TeV_EGAM1_probes_lhmedium_EGAM7_vetolhvloose.py --Zee'
command_2="python job_correction_v10_data17_13TeV_EGAM1_probes_lhmedium_EGAM7_vetolhvloose.py --egam7"


BASEPATH_EGAM1='/afs/cern.ch/work/j/jodafons/public/data17_13TeV/PhysVal_v2/EGAM1'
BASEPATH_EGAM7='/afs/cern.ch/work/j/jodafons/public/data17_13TeV/PhysVal_v2/EGAM7'



python prun_jobs.py -i $BASEPATH_EGAM1  -c $command_1 -mt 70
mkdir egam1
python prun_merge.py -i output_* -o egam1.root -nm 35 -mt 10
mv *.root egam1





