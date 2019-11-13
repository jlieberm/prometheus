__all__ = ['nvtx_bins','zee_etbins','jpsiee_etbins','coarse_etbins','default_etabins','ringer_tuning_etbins',
          'ringer_tuning_etabins', 'RingerLayers','ringLowerEdges','ringHighEdges','ringNBins',
          'lh_thres_etabins', 'lh_thres_etbins', 'lh_tuning_etabins', 'lh_tuning_etbins',
          'standardQuantitiesEtaEdge', 'standardQuantitiesHighEdges', 'standardQuantitiesLowerEdges',
          'standardQuantitiesSpecialBins', 'standardQuantitiesNBins', 'standardQuantitiesPDFsHighEdges',
          'standardQuantitiesPDFsLowerEdges', 'standardQuantitiesPDFsNBins', 'specialElectronBins', 'basicInfoQuantities',
          'basicInfoNBins', 'basicInfoLowerEdges', 'basicInfoHighEdges','fudge_etbins','fudge_etabins',
          'scalefactor_etbins','scalefactor_etabins','high_nvtx_bins', 'electronLatexStr', 'basicInfoLatexStr',
          'electronQuantities']

import math


# Ringer layer edges
class RingerLayers(object):
  PreSampler = (0,7)
  EM1  = (8,71)
  EM2  = (72,79)
  EM3  = (80,87)
  HAD1 = (88,91)
  HAD2 = (92,95)
  HAD3 = (96,99)

ringLowerEdges = [ -1000., -1000., -1000., -1000., -1000., -1000., -1000., -900.   # PS
                 , -2500., -2500., -1500., -1500., -1500., -1500., -2000., -2000.  # EM1
                 , -2000., -2000., -800.,  -800.,  -800.,  -800.,  -800.,  -800.   # EM1
                 , -800.,  -800.,  -800.,  -800.,  -800.,  -800.,  -800.,  -700.   # EM1
                 , -600.,  -600.,  -600.,  -600.,  -600.,  -600.,  -600.,  -600.   # EM1
                 , -600.,  -600.,  -600.,  -500.,  -500.,  -500.,  -500.,  -500.   # EM1
                 , -500.,  -500.,  -500.,  -500.,  -500.,  -400.,  -400.,  -400.   # EM1
                 , -400.,  -400.,  -400.,  -400.,  -400.,  -400.,  -300.,  -300.   # EM1
                 , -300.,  -300.,  -300.,  -300.,  -300.,  -300.,  -300.,  -300.   # EM1
                 , -1000., -1000., -1000., -1500., -2000., -2000., -2000., -2000.  # EM2
                 , -900.,  -900.,  -900.,  -900.,  -900.,  -900.,  -800.,  -800.   # EM3
                 , -3000., -3000., -3000., -3000. # HAD1
                 , -2000., -2000., -2000., -2000. # HAD2
                 , -1000., -1000., -1000., -1000. # HAD2
                 ] # all

ringHighEdges = [ 14000., 14000., 8000.,  7000.,  6500.,  6000., 5500., 5000.  # PS
                , 17000., 15000., 12000., 9000.,  9000.,  7000., 6500., 5500.  # EM1
                , 8500.,  5000.,  5000.,  5000.,  5000.,  4500., 4500., 4500.  # EM1
                , 4000.,  4000.,  4000.,  4000.,  4000.,  3500., 3500., 3500.  # EM1
                , 3500.,  3500.,  3500.,  3500.,  3500.,  3500., 3500., 3500.  # EM1
                , 3500.,  3500.,  3500.,  3000.,  3000.,  3000., 3000., 3000.  # EM1
                , 3000.,  3000.,  3000.,  3000.,  2500.,  2500., 2500., 2500.  # EM1
                , 2500.,  2500.,  2500.,  2200.,  2200.,  2200., 2200., 2200.  # EM1
                , 2200.,  2200.,  2200.,  2200.,  2200.,  2000., 2000., 2000.  # EM1
                , 80000., 80000., 40000., 25000., 18000., 18000.,12500.,12000. # EM2
                , 14000., 12000., 8000.,  7000.,  5000.,  4500., 4200., 4000.  # EM3
                , 60000., 60000., 30000., 22000.  # HAD1
                , 60000., 60000., 25000., 20000.  # HAD2
                , 25000., 30000., 15000., 12000.  # HAD3
                ] # all

ringNBins = [60]*100

# Values retrieved from analysis trigger tool
default_etabins= [-2.47,-2.37,-2.01,-1.81,-1.52,-1.37,-1.15,-0.80,-0.60,-0.10,0.00,
                   0.10, 0.60, 0.80, 1.15, 1.37, 1.52, 1.81, 2.01, 2.37, 2.47]

coarse_etbins = [4.,7.,10.,15.,20.,25.,30.,35.,40.,45.,50.,60.,80.,150.]

zee_etbins = [0.,2.,4.,6.,8.,10.,12.,14.,16.,18.,20.,22.,24.,26.,28.,
             30.,32.,34.,36.,38.,40.,42.,44.,46.,48.,50.,55.,60.,65.,70.,100.]



jpsiee_etbins =[ 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5,
                 8.0, 8.5, 9.0, 9.5, 10.0,10.5,11.0,11.5,12.0,12.5,13.0,13.5,14.0,14.5, 15.0]

nvtx_bins = [                                         -0.5,
          0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5,
         10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,
         20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,
         30.5,31.5,32.5,33.5,34.5,35.5,36.5,37.5,38.5,39.5,
         40.5,41.5,42.5,43.5,44.5,45.5,46.5,47.5,48.5,49.5,
         50.5,51.5,52.5,53.5,54.5,55.5,56.5,57.5,58.5,59.5,
         60.5]

high_nvtx_bins = [61.5,62.5,63.5,64.5,65.5,66.5,67.5,68.5,69.5,70.5,
                  71.5,72.5,73.5,74.5,75.5,76.5,77.5,78.5,79.5,80.5,
                  81.5,82.5,83.5,84.5,85.5,86.5,87.5,88.5,89.5,90.5,
                  91.5,92.5,93.5,94.5,95.5,96.5,97.5,98.5,99.5,100.5]

# The first ringer binning approch used in MC15c 2016/2017
#ringer_tuning_etbins    = [15, 20, 30, 40, 50, 1e5 ]
#ringer_tuning_etabins   = [0, 0.8 , 1.37, 1.54, 2.47]

# The second ringer binning approch used in MC16d and data17_13TeV 2018
ringer_tuning_etbins    = [15, 20, 30, 40, 50, 1e5 ]
ringer_tuning_etabins   = [0, 0.8 , 1.37, 1.54, 2.37 ,2.47]


lh_tuning_etbins        = [4,7,10,15,20,30,40,50000]
lh_tuning_etabins       = [0.00,0.60,0.80,1.15,1.37,1.52,1.81,2.01,2.37,2.47]

lh_thres_etbins         = [4,7,10,15,20,25,30,35,40,45,50,50000]
lh_thres_etabins        = [0.00,0.60,0.80,1.15,1.37,1.52,1.81,2.01,2.37,2.47]

fudge_etbins            = [15, 20, 30, 40, 50, 1e5 ]
fudge_etabins           = [0, 0.8 , 1.37, 1.54, 2.37, 2.47]


scalefactor_etbins      = [15.0, 20.0, 30.0, 40.0, 50.0, 150.0 ]
scalefactor_etabins     = [-2.47, -2.37, -1.54, -1.37, -0.8, 0.0,  0.8 , 1.37, 1.54, 2.37, 2.47]




nEtaLHTuning = len(lh_tuning_etabins) - 1
nEtLHTuning =  len(lh_tuning_etbins) - 1

standardQuantitiesSpecialBins = {
      "f1" : [0.],
      "f3" : [0.],
      "reta" : [1.],
      "rphi" : [1.],
      "eratio" : [0.,1.],
      "TRT_PID" : [0.],
      "deltaPoverP" : [0.]
      }

standardQuantitiesEtaEdge = {
    "f3" : 2.37,
    "TRT_PID" : 2.01
    }

# TODO Check if quantites name match
standardQuantitiesLowerEdges = { "f1":                         -0.02,
                                "f3":                         -0.05,
                                "weta2":                      0.005,
                                "wtots1":                     0.00,
                                "reta":                       0.80,
                                "rhad":                       -0.05,
                                "rphi":                       0.45,
                                "eratio":                     0.50,
                                "deltaEta1":                  -0.01,
                                "deltaPhiRescaled2":          -0.03,
                                "trackd0pvunbiased":          -0.50,
                                "d0significance":             0.00,
                                "eProbabilityHT":             -0.05,
                                "TRT_PID":                    -1.00,
                                "DeltaPOverP":                -1.2,
                              }
standardQuantitiesHighEdges = {
                              "f1":                        0.7,
                              "f3":                        0.15,
                              "weta2":                     0.02,
                              "wtots1":                    8.00,
                              "reta":                      1.10,
                              "rhad":                      0.05,
                              "rphi":                      1.05,
                              "eratio":                    1.05,
                              "deltaEta1":                 0.01,
                              "deltaPhiRescaled2":         0.03,
                              "trackd0pvunbiased":         0.50,
                              "d0significance":            10.00,
                              "eProbabilityHT":            1.05,
                              "TRT_PID" :                  1.00,
                              "DeltaPOverP":               1.2,
                              }

standardQuantitiesNBins = {
                           "f1":                    100,
                           "f3":                    200,
                           "weta2":                 100,
                           "wtots1":                100,
                           "reta":                  200,
                           "rhad":                  200,
                           "rphi":                  200,
                           "eratio":                100,
                           "deltaEta1":             200,
                           "deltaPhiRescaled2":     200,
                           "trackd0pvunbiased":     200,
                           "d0significance":        100,
                           "eProbabilityHT":        100,
                           "TRT_PID" :              100,
                           "DeltaPOverP":           100,
                          }

standardQuantitiesPDFsLowerEdges = {
    "deltaEmax2": [[0.,  0.,  0.,  0., 0.,  0., 0.5, 0.8,  0.], # 4
                   [0.,  0.,  0.,  0., 0.,  0., 0.5, 0.8,  0.], # 7
                   [0.,  0.,  0.,  0., 0.,  0., 0.5, 0.8,  0.], # 10
                   [0.,  0.,  0.,  0., 0.,  0., 0.5, 0.8,  0.], # 15
                   [0.,  0.,  0.,  0., 0.,  0., 0.8, 0.8,  0.], # 20
                   [0.,  0.,  0.,  0., 0.,  0., 0.8, 0.85, 0.], # 30
                   [0.,  0.,  0.,  0., 0.,  0., 0.8, 0.85, 0.]],
    "eratio": [[0.,  0.,  0.,  0., 0.,  0., 0.5, 0.8,  0.], # 4
               [0.,  0.,  0.,  0., 0.,  0., 0.5, 0.8,  0.], # 7
               [0.,  0.,  0.,  0., 0.,  0., 0.5, 0.8,  0.], # 10
               [0.,  0.,  0.,  0., 0.,  0., 0.5, 0.8,  0.], # 15
               [0.,  0.,  0.,  0., 0.,  0., 0.8, 0.8,  0.], # 20
               [0.,  0.,  0.,  0., 0.,  0., 0.8, 0.85, 0.], # 30
               [0.,  0.,  0.,  0., 0.,  0., 0.8, 0.85, 0.]],
    "weta2": [[0.006,  0.006,  0.006,  0.006, 0.00,  0.006,  0.006,  0.006,  0.006 ], # 4
              [0.006,  0.006,  0.006,  0.006, 0.00,  0.006,  0.006,  0.006,  0.006 ], # 7
              [0.006,  0.006,  0.006,  0.006, 0.00,  0.006,  0.006,  0.006,  0.006 ], # 10
              [0.006,  0.006,  0.006,  0.006, 0.00,  0.006,  0.006,  0.006,  0.006 ], # 15
              [0.006,  0.006,  0.006,  0.006, 0.00,  0.006,  0.006,  0.006,  0.006 ], # 20
              [0.006,  0.006,  0.006,  0.006, 0.00,  0.006,  0.006,  0.006,  0.006 ], # 30
              [0.006,  0.006,  0.006,  0.006, 0.00,  0.006,  0.006,  0.006,  0.006 ]], # 40
    "ws3": [[0.3,  0.3,  0.3,  0.3, 0.00,  0.3,  0.3,  0.3,  0.3 ], # 4
            [0.3,  0.3,  0.3,  0.3, 0.00,  0.3,  0.3,  0.3,  0.3 ], # 7
            [0.3,  0.3,  0.3,  0.3, 0.00,  0.3,  0.3,  0.3,  0.3 ], # 10
            [0.3,  0.3,  0.3,  0.3, 0.00,  0.3,  0.3,  0.3,  0.3 ], # 15
            [0.3,  0.3,  0.3,  0.3, 0.00,  0.3,  0.3,  0.3,  0.3 ], # 20
            [0.3,  0.3,  0.3,  0.3, 0.00,  0.3,  0.3,  0.3,  0.3 ], # 30
            [0.3,  0.3,  0.3,  0.3, 0.00,  0.3,  0.3,  0.3,  0.3 ]], # 40
    "deltaEta1": [[-0.1]*nEtaLHTuning]*nEtLHTuning,
    "f1": [[-0.05]*nEtaLHTuning]*nEtLHTuning,
    "f3": [[-0.02]*nEtaLHTuning]*nEtLHTuning,
    "fside": [[-0.2]*nEtaLHTuning]*nEtLHTuning,
    "deltaPhi2": [[-0.1]*nEtaLHTuning]*nEtLHTuning,
    "reta": [[0.5]*nEtaLHTuning]*nEtLHTuning,
    "rhad": [[ -0.075 ]*nEtaLHTuning]*nEtLHTuning,
    "rphi": [[ 0.45 ]*nEtaLHTuning]*nEtLHTuning,
    "wstot": [[ 0.]*nEtaLHTuning]*nEtLHTuning,
    "d0significance": [[ 0.]*nEtaLHTuning]*nEtLHTuning,
    "TRTHighTHitsRatio": [[ 0.0 ]*nEtaLHTuning]*nEtLHTuning,
    "TRTHighTOutliersRatio": [[ 0.0 ]*nEtaLHTuning]*nEtLHTuning,
    "trackd0pvunbiased": [[ -1. ]*nEtaLHTuning]*nEtLHTuning,
    "deltaPoverP": [[ -0.2 ]*nEtaLHTuning]*nEtLHTuning,
    "ptcone20pt": [[ 0. ]*nEtaLHTuning]*nEtLHTuning,
    "EoverP": [[ 0. ]*nEtaLHTuning]*nEtLHTuning,
    "PassBL": [[ 0. ]*nEtaLHTuning]*nEtLHTuning,
    "deltaphiRescaled": [[ -0.150 ]*nEtaLHTuning]*nEtLHTuning,
}

standardQuantitiesPDFsHighEdges = {
  "f1":    [[ 0.65,   0.6,   0.5,   0.5, 0.55,   0.55, 0.55, 0.65, 0.5 ],  #4
            [ 0.65,   0.6,   0.5,   0.5, 0.55,   0.55, 0.55, 0.65, 0.5 ],  #7
            [ 0.65,   0.6,   0.5,   0.5, 0.55,   0.55, 0.55, 0.65, 0.5 ],  #10
            [ 0.65,   0.6,   0.5,   0.5, 0.55,   0.55, 0.55, 0.65, 0.5 ],  #15
            [ 0.65,   0.6,   0.5,   0.5, 0.55,   0.55, 0.55, 0.65, 0.5 ],  #20
            [ 0.65,   0.6,   0.5,   0.5, 0.55,   0.55, 0.55, 0.65, 0.5 ],  #30
            [ 0.65,   0.6,   0.5,   0.5, 0.55,   0.55, 0.55, 0.65, 0.5 ]], #40
  "weta2":    [[0.018,  0.018,  0.018,  0.018, 0.030,  0.018,  0.018,  0.018,  0.018 ], # 4
               [0.018,  0.018,  0.018,  0.018, 0.030,  0.018,  0.018,  0.018,  0.018 ], # 7
               [0.018,  0.018,  0.018,  0.018, 0.030,  0.018,  0.018,  0.018,  0.018 ], # 10
               [0.018,  0.018,  0.018,  0.018, 0.030,  0.018,  0.018,  0.018,  0.018 ], # 15
               [0.018,  0.018,  0.018,  0.018, 0.030,  0.018,  0.018,  0.018,  0.018 ], # 20
               [0.018,  0.018,  0.018,  0.018, 0.030,  0.018,  0.018,  0.018,  0.018 ], # 30
               [0.018,  0.018,  0.018,  0.018, 0.030,  0.018,  0.018,  0.018,  0.018 ]], # 40
  "ws3":    [[1.,  1.,  1.,  1., 1.,  1.,  1.,  1.,  1. ], # 4
             [1.,  1.,  1.,  1., 1.,  1.,  1.,  1.,  1. ], # 7
             [1.,  1.,  1.,  1., 1.,  1.,  1.,  1.,  1. ], # 10
             [1.,  1.,  1.,  1., 1.,  1.,  1.,  1.,  1. ], # 15
             [1.,  1.,  1.,  1., 1.,  1.,  1.,  1.,  1. ], # 20
             [1.,  1.,  1.,  1., 1.,  1.,  1.,  1.,  1. ], # 30
             [1.,  1.,  1.,  1., 1.,  1.,  1.,  1.,  1. ]], # 40
  "deltaeta1": [[ 0.1 ]*nEtaLHTuning]*nEtLHTuning,
  "f3": [[ 0.15]*nEtaLHTuning]*nEtLHTuning,
  "fside": [[ 1.5]*nEtaLHTuning]*nEtLHTuning,
  "deltaphi2": [[ 0.05]*nEtaLHTuning]*nEtLHTuning,
  "reta": [[ 1.5]*nEtaLHTuning]*nEtLHTuning,
  "rhad": [[ 0.2]*nEtaLHTuning]*nEtLHTuning,
  "rphi": [[ 1.05]*nEtaLHTuning]*nEtLHTuning,
  "wstot": [[ 8.]*nEtaLHTuning]*nEtLHTuning,
  "d0Sig": [[ 20.]*nEtaLHTuning]*nEtLHTuning,
  "d0significance": [[ 20.]*nEtaLHTuning]*nEtLHTuning,
  "TRTHighTHitsRatio": [[0.5]*nEtaLHTuning]*nEtLHTuning,
  "TRTHighTOutliersRatio": [[0.5]*nEtaLHTuning]*nEtLHTuning,
  "trackd0": [[ 1.]*nEtaLHTuning]*nEtLHTuning,
  "trackd0_physics": [[ 1.]*nEtaLHTuning]*nEtLHTuning,
  "trackd0pvunbiased": [[ 1.]*nEtaLHTuning]*nEtLHTuning,
  "deltaEmax2": [[ 1.]*nEtaLHTuning]*nEtLHTuning,
  "eratio": [[ 1.]*nEtaLHTuning]*nEtLHTuning,
  "ptcone20pt": [[ 0.5]*nEtaLHTuning]*nEtLHTuning,
  "EoverP": [[ 8.]*nEtaLHTuning]*nEtLHTuning,
  "PassBL": [[ 2.]*nEtaLHTuning]*nEtLHTuning,
  "deltaphiRescaled": [[0.150]*nEtaLHTuning]*nEtLHTuning,
  #"deltaPoverP": [[1.2]*nEtaLHTuning]*nEtLHTuning,
  "deltaPoverP": [[1.0]*nEtaLHTuning]*nEtLHTuning,
  "eProbabilityHT": [[1]*nEtaLHTuning]*nEtLHTuning,
  "TRT_PID": [[0.96]*nEtaLHTuning]*nEtLHTuning,
  "TRT_PID_significance": [[0.3]*nEtaLHTuning]*nEtLHTuning,
  }

standardQuantitiesPDFsNBins = {
  "deltaeta1": 500, "f3": 500, "fside": 500,
  "deltaphi2": 500, "reta": 500, "rhad": 500,
  "rphi": 500, "wstot": 500, "d0Sig": 500,
  "d0significance": 500, "TRTHighTHitsRatio": 60, "TRTHighTOutliersRatio": 60,
  "trackd0": 500, "trackd0_physics": 500, "trackd0pvunbiased": 500,
  "ptcone20pt": 500, "EoverP": 500, "PassBL": 500,
  "deltaphiRescaled": 500, "deltaPoverP": 500, "MVAResponse": 500,
  "cl_phi": 500, "eProbabilityHT": 500, "TRT_PID": 500,
  "TRT_PID_significance": 500, "deltaEmax2": 500, "eratio": 500,
  "f0": 500, "f1": 500, "weta2": 500,
  "ws3": 500, }

standardQuantitiesLowerEdges = { "f1":                         -0.02,
                                "f3":                         -0.05,
                                "weta2":                      0.005,
                                "wtots1":                     0.00,
                                "reta":                       0.80,
                                "rhad":                       -0.05,
                                "rphi":                       0.45,
                                "eratio":                     0.50,
                                "deltaEta1":                  -0.01,
                                "deltaPhiRescaled2":          -0.03,
                                "trackd0pvunbiased":          -0.50,
                                "d0significance":             0.00,
                                "eProbabilityHT":             -0.05,
                                "TRT_PID":                    -1.00,
                                "DeltaPOverP":                -1.2,
                              }
standardQuantitiesHighEdges = {
                              "f1":                        0.7,
                              "f3":                        0.15,
                              "weta2":                     0.02,
                              "wtots1":                    8.00,
                              "reta":                      1.10,
                              "rhad":                      0.05,
                              "rphi":                      1.05,
                              "eratio":                    1.05,
                              "deltaEta1":                 0.01,
                              "deltaPhiRescaled2":         0.03,
                              "trackd0pvunbiased":         0.50,
                              "d0significance":            10.00,
                              "eProbabilityHT":            1.05,
                              "TRT_PID" :                  1.00,
                              "DeltaPOverP":               1.2,
                              }

standardQuantitiesNBins = {
                           "f1":                    100,
                           "f3":                    200,
                           "weta2":                 100,
                           "wtots1":                100,
                           "reta":                  200,
                           "rhad":                  200,
                           "rphi":                  200,
                           "eratio":                100,
                           "deltaEta1":             200,
                           "deltaPhiRescaled2":     200,
                           "trackd0pvunbiased":     200,
                           "d0significance":        100,
                           "eProbabilityHT":        100,
                           "TRT_PID" :              100,
                           "DeltaPOverP":           100,
                          }

specialElectronBins = { 'f1' : [0]
                      , 'f3' : [0]
                      , 'reta' : [1]
                      , 'rphi' : [1]
                      , 'eratio' : [0,1]
                      , 'TRT_PID' : [0]
                      , 'deltaPOverP' : [0]
                      }

basicInfoNBins = { "et":         100,
                   "eta":        100,
                   "phi":        100,
                   "avgmu":      62,
                   "nvtx":       62,       }

basicInfoLowerEdges = { "et":    0,
                        "eta":   -2.5,
                        "phi":   -math.pi,
                        "avgmu": -0.5,
                        "nvtx":  -0.5,     }

basicInfoHighEdges = { "et":     100,
                       "eta":    2.5,
                       "phi":    math.pi,
                       "avgmu":  60.5,
                       "nvtx":   60.5,     }



# As found in PlotVariables
electronQuantities = { 'et' : 'E_{T}'
                     , 'eta' : '#eta'
                     , 'phi' : '#phi'
                     , 'rhad' : 'R_{had}'
                     , 'reta' : 'R_{#eta}'
                     , 'deltaEta1' : '#Delta#eta_{1}'
                     , 'weta2': 'w_{#eta,2}'
                     , 'wtots1': 'w_{tots,1}'
                     , 'f1' : 'f_{1}'
                     , 'rphi' : 'R_{#phi}'
                     , 'f3' : 'f_{3}'
                     , 'eratio' : 'E_{ratio}'
                     , 'deltaPhiRescaled2' : '#Delta#phi_{res}'
                     , 'd0significance' : 'd_{0}/#sigma_{d_{0}}'
                     , 'trackd0pvunbiased' : 'd_{0}'
                     , 'eProbabilityHT' :  'eProbabilityHT'
                     , 'TRT_PID' : 'TRT_{PID}'
                     , 'DeltaPOverP' : '#Delta p/p'
                     }

def electronLatexStr(var):
  try:
    return electronQuantities[var]
  except KeyError as e:
    raise KeyError( 'Latex string is unavailable for quantity: %s' % str(var) )

basicInfoQuantities = { 'et' : 'E_{T}'
                      , 'eta' : '#eta'
                      , 'phi' : '#phi'
                      , 'avgmu' : '<#mu>'
                      , 'nvtx' : '# Primary Vertices'
                      }

def basicInfoLatexStr(var):
  try:
    return basicInfoQuantities[var]
  except KeyError as e:
    raise KeyError( 'Latex string is unavailable for quantity: %s' % str(var) )



