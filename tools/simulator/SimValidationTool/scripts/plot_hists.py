



f = 'hist.root'


from ValidationTool.drawers import *
from Gaugi.storage import  restoreStoreGate
#store1 =  restoreStoreGate( f1 )
sg =  restoreStoreGate( f )

from monet.AtlasStyle import SetAtlasStyle
SetAtlasStyle()


PlotShowers( sg.histogram("Zee/Profiles/et"), sg.histogram("JF17/Profiles/et")  , 'Z#rightarrow ee','JF17','E_{T} [GeV]','et.pdf' , doLogY=False )
PlotShowers( sg.histogram("Zee/Profiles/eta"), sg.histogram("JF17/Profiles/eta")  , 'Z#rightarrow ee','JF17','#eta','eta.pdf'     , doLogY=False)
PlotShowers( sg.histogram("Zee/Profiles/eratio"), sg.histogram("JF17/Profiles/eratio")  , 'Z#rightarrow ee','JF17','E_{ratio}','eratio.pdf' )
PlotShowers( sg.histogram("Zee/Profiles/reta")  , sg.histogram("JF17/Profiles/reta")    , 'Z#rightarrow ee','JF17','R_{#eta}' ,'reta.pdf'   )
PlotShowers( sg.histogram("Zee/Profiles/rphi")  , sg.histogram("JF17/Profiles/rphi")    , 'Z#rightarrow ee','JF17','R_{#phi}' ,'rphi.pdf'   )
PlotShowers( sg.histogram("Zee/Profiles/rhad")  , sg.histogram("JF17/Profiles/rhad")    , 'Z#rightarrow ee','JF17','R_{had}'  ,'rhad.pdf'   )
PlotShowers( sg.histogram("Zee/Profiles/f1")    , sg.histogram("JF17/Profiles/f1")      , 'Z#rightarrow ee','JF17','f_{1}' ,'f1.pdf'     )
PlotShowers( sg.histogram("Zee/Profiles/f3")    , sg.histogram("JF17/Profiles/f3")      , 'Z#rightarrow ee','JF17','f_{3}' ,'f3.pdf'     )

PlotShowers( sg.histogram("Zee/Profiles/rings/rings_profile"), sg.histogram("JF17/Profiles/rings/rings_profile"), 
    'Z#rightarrow ee','JF17','#ring' ,'rings_profile.pdf', ylabel='Energy Average [GeV]'  )

PlotShowers( sg.histogram("Zee/Profiles/rings/rings_profile"), sg.histogram("JF17/Profiles/rings/rings_profile"), 
    'Z#rightarrow ee','JF17','#ring' ,'rings_profile_nolog.pdf', ylabel='Energy Average [GeV]' , doLogY=False )


