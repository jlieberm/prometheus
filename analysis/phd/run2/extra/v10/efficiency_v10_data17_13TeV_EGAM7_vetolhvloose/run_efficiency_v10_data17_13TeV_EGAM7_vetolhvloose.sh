

prun \
     --exec \
       "sh -c '. /setup_envs.sh && python /code/prometheus/analysis/phd/run2/extra/v10/efficiency_v10_data17_13TeV_EGAM7_vetolhvloose/job_efficiency_v10_data17_13TeV_EGAM7_vetolhvloose.py -i %IN -o output.root';" \
     --excludedSite=ANALY_DESY-HH_UCORE,ANALY_MWT2_SL6,ANALY_MWT2_HIMEM,ANALY_DESY-HH,ANALY_FZK_UCORE,ANALY_FZU,DESY-HH_UCORE,FZK-LCG2_UCORE \
     --containerImage=docker://jodafons/prometheus:lcg \
     --noBuild \
     --inDS=user.jodafons.data17_13TeV.physics_Main.deriv.DAOD_EGAM7.after_ts1.Physval.GRL_v97.r7001 \
      --outDS=user.jodafons.efficiency_v10_data17_13TeV_EGAM7_vetolhvloose.after_ts1.test_1 \
     --disableAutoRetry \
     --outputs="output:output.root" \
     --nFilesPerJob=2 \
     --forceStaged \
     --mergeOutput \
     --site AUTO \





