

BASEPATH_Zee=/eos/user/j/jodafons/CERN-DATA/data/mc15_13TeV/PhysVal_v2/user.jodafons.mc15_13TeV.361106.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zee.merge.AOD.e3601_s2876_r7917_r7676.PhysVal_v2/*

BASEPATH_JF17=/eos/user/j/jodafons/CERN-DATA/data/mc15_13TeV/PhysVal_v2/user.jodafons.mc15_13TeV.423300.Pythia8EvtGen_A14NNPDF23LO_perf_JF17.merge.AOD.e3848_s2876_r7917_r7676.PhysVal_v2/*


command_1="python3 job_collector_v6.py --Zee"
command_2="python3 job_collector_v6.py --jf17"

prun_jobs.py -i $BASEPATH_Zee -c $command_1 -mt 30
#prun_jobs.py -i $BASEPATH_JF17 -c $command_2 -mt 30











