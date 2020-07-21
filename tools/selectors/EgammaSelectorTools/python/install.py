

__all__ = [
           "installTrigEgammaSelectors_Run2",
           ]

from Gaugi import GeV

# Install the LH HLT selector
def installTrigEgammaSelectors_Run2( toolname = "Emulator" ):

  from EgammaSelectorTools import TrigEgammaL1CaloSelectorTool
  from EgammaSelectorTools import TrigEgammaL2CaloSelectorTool
  from EgammaSelectorTools import TrigEgammaL2ElectronSelectorTool
  from EgammaSelectorTools import TrigEgammaElectronSelectorTool
  
  selectors = [

      # L1Calo selector + et cuts
      TrigEgammaL1CaloSelectorTool('L1_EM3'               , L1Item = 'L1_EM3'     ),
      TrigEgammaL1CaloSelectorTool('L1_EM22VH'            , L1Item = 'L1_EM22VH'  ),
      TrigEgammaL1CaloSelectorTool('L1_EM22VHI'           , L1Item = 'L1_EM22VHI' ),
      TrigEgammaL1CaloSelectorTool('L1_EM15VH'            , L1Item = 'L1_EM15VH'  ),
      TrigEgammaL1CaloSelectorTool('L1_EM15VHI'           , L1Item = 'L1_EM15VHI' ),
      
      # L2Calo selector only (backward)
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloTight"           , IDinfo='lhtight'  ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloMedium"          , IDinfo='lhmedium' ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloLoose"           , IDinfo='lhloose'  ) ,
      TrigEgammaL2CaloSelectorTool("T0HLTElectronT2CaloVLoose"          , IDinfo='lhvloose' ) ,

 
      # L2Calo selector only (backward)
      TrigEgammaL2CaloSelectorTool("L2Calo_LHTight"       , IDinfo='lhtight'  ) ,
      TrigEgammaL2CaloSelectorTool("L2Calo_LHMedium"      , IDinfo='lhmedium' ) ,
      TrigEgammaL2CaloSelectorTool("L2Calo_LHLoose"       , IDinfo='lhloose'  ) ,
      TrigEgammaL2CaloSelectorTool("L2Calo_LHVLoose"      , IDinfo='lhvloose' ) ,


      TrigEgammaL2ElectronSelectorTool('L2_Electron_below15GeV',
                                        EtCut                =   0    , 
                                        TrackPt              =   1*GeV, 
                                        CaloTrackdETA        =   0.2  , 
                                        CaloTrackdPHI        =   0.3  , 
                                        CaloTrackdEoverPLow  =   0    , 
                                        CaloTrackdEoverPHigh =   999  , 
                                        TRTRatio             =   -999 ),

      TrigEgammaL2ElectronSelectorTool('L2_Electron_15to20GeV',
                                        EtCut                =   0    , 
                                        TrackPt              =   2*GeV, 
                                        CaloTrackdETA        =   0.2  , 
                                        CaloTrackdPHI        =   0.3  , 
                                        CaloTrackdEoverPLow  =   0    , 
                                        CaloTrackdEoverPHigh =   999  , 
                                        TRTRatio             =   -999 ),

      TrigEgammaL2ElectronSelectorTool('L2_Electron_20to50GeV',
                                        EtCut                =   0    , 
                                        TrackPt              =   3*GeV, 
                                        CaloTrackdETA        =   0.2  , 
                                        CaloTrackdPHI        =   0.3  , 
                                        CaloTrackdEoverPLow  =   0    , 
                                        CaloTrackdEoverPHigh =   999  , 
                                        TRTRatio             =   -999 ),

      TrigEgammaL2ElectronSelectorTool('L2_Electron_above50GeV',
                                        EtCut                =   0    , 
                                        TrackPt              =   5*GeV, 
                                        CaloTrackdETA        =   999  , 
                                        CaloTrackdPHI        =   999  , 
                                        CaloTrackdEoverPLow  =   0    , 
                                        CaloTrackdEoverPHigh =   999  , 
                                        TRTRatio             =   -999 ),

 

      # HLT Electron selector only
      TrigEgammaElectronSelectorTool('HLT_LHTight'          , branch = 'trig_EF_el_lhtight'   ),
      TrigEgammaElectronSelectorTool('HLT_LHMedium'         , branch = 'trig_EF_el_lhmedium'  ),
      TrigEgammaElectronSelectorTool('HLT_LHLoose'          , branch = 'trig_EF_el_lhloose'   ),
      TrigEgammaElectronSelectorTool('HLT_LHVLoose'         , branch = 'trig_EF_el_lhvloose'  ),
      TrigEgammaElectronSelectorTool('HLT_LHTightCaloOnly'  , branch = 'trig_EF_calo_lhtight' ),
      TrigEgammaElectronSelectorTool('HLT_LHMediumCaloOnly' , branch = 'trig_EF_calo_lhmedium'),
      TrigEgammaElectronSelectorTool('HLT_LHLooseCaloOnly'  , branch = 'trig_EF_calo_lhloose' ),
      TrigEgammaElectronSelectorTool('HLT_LHVLooseCaloOnly' , branch = 'trig_EF_calo_lhvloose'),
      
      
      ]
  from Gaugi import ToolSvc as toolSvc
  tool = toolSvc.retrieve( toolname )
  if tool:
    for sel in selectors:
      tool+=sel
  else:
    raise RuntimeError("%s not found into the ToolSvc." % toolname)




