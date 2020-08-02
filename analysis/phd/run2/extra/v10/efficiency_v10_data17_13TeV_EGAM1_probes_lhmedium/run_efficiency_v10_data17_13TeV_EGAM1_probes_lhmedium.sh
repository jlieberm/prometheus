
prun_lcg.py \
  --command  "sh -c '. /setup_envs.sh && python /code/prometheus/analysis/phd/run2/extra/v10/efficiency_v10_data17_13TeV_EGAM1_probes_lhmedium/job_efficiency_v10_data17_13TeV_EGAM1_probes_lhmedium.py -i %IN -o output.root';" \
  --inDS=user.jodafons.data17_13TeV.physics_Main.deriv.DAOD_EGAM1.after_ts1.Physval.GRL_v97.r7001 \
  --outDS=user.jodafons.efficiency_v10_data17_13TeV_EGAM1_probes_lhmedium.test_1 \
  --nFilesPerJob=2 \
  --outputs "output:output.root" \
  --dry_run \

  






