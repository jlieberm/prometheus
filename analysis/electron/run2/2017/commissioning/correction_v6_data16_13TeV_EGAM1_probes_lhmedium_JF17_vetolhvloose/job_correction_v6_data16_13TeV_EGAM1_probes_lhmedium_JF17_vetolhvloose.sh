

BASEPATH_ZEE=../cern_data/mc15_13TeV/PhysVal_v2/user.jodafons.mc15_13TeV.361106.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zee.merge.AOD.e3601_s2876_r7917_r7676.PhysVal_v2
BASEPATH_JF17=../cern_data/mc15_13TeV/PhysVal_v2/user.jodafons.mc15_13TeV.423300.Pythia8EvtGen_A14NNPDF23LO_perf_JF17.merge.AOD.e3848_s2876_r7917_r7676.PhysVal_v2
BASEPATH_EGAM1=../cern_data/data16_13TeV/PhysVal_v2

command_1="python job_correction_v6_data16_13TeV_EGAM1_probes_lhmedium_JF17_vetolhvloose.py --Zee"
command_2="python job_correction_v6_data16_13TeV_EGAM1_probes_lhmedium_JF17_vetolhvloose.py --Zee --egam7"

#prun_jobs.py -i $BASEPATH_ZEE  -c $command_1 -mt 32 
#mkdir zee
#prun_merge.py -i output_* -o zee.root -nm 35 -mt 10
#mv *.root zee

prun_jobs.py -i $BASEPATH_JF17  -c $command_2 -mt 32
mkdir jf17
prun_merge.py -i output_* -o jf17.root -nm 35 -mt 10
mv *.root jf17

prun_jobs.py -i $BASEPATH_EGAM1  -c $command_1 -mt 32
mkdir egam1
prun_merge.py -i output_* -o egam1.root -nm 35 -mt 10
mv *.root egam1





