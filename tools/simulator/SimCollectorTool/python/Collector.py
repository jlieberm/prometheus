
__all__ = ["Collector"]

from Gaugi import Algorithm
from Gaugi import StatusCode, NotSet, retrieve_kw
from Gaugi.messenger.macros import *
from EventSimulator import *
import numpy as np


class Collector( Algorithm ):

  def __init__(self, name, **kw):
    Algorithm.__init__(self, name)
    self._outputname  =retrieve_kw( kw , 'outputname', 'collection.pic')
    self._event = []

  def initialize(self):
  
    self._event_label = ['avgmu']
    self._event_label.extend( [ 'ring_%d'%r for r in range(92) ] )
    self._event_label.extend( [ 
                                'et',
                                'eta',
                                'phi',
                                'eratio',
                                'reta',
                                'rphi',
                                'rhad',
                                'f1',
                                'f3',
                                'weta2',
                                'ehad1',
                                'ehad2',
                                'ehad3',
                                ] )


    return StatusCode.SUCCESS


  def fill( self, event ):
    self._event.append(event)


  def execute(self, context):
    
    event = self.getContext().getHandler( "EventInfoContainer" )
    cluster = self.getContext().getHandler( "Truth__CaloClusterContainer" )
    ringer = self.getContext().getHandler( "Truth__CaloRingsContainer" )
    
    if cluster.isValid() and ringer.isValid():
    
      event_row = list() 
      event_row.append( event.avgmu() )
      event_row.extend( ringer.ringsE() )
      event_row.append( cluster.et() )
      event_row.append( cluster.eta() )
      event_row.append( cluster.phi() )
      event_row.append( cluster.eratio() )
      event_row.append( cluster.reta() )
      event_row.append( cluster.rphi() )
      event_row.append( cluster.rhad() )
      event_row.append( cluster.f1() )
      event_row.append( cluster.f3() )
      event_row.append( cluster.weta2() )
      event_row.append( cluster.ehad1() )
      event_row.append( cluster.ehad2() )
      event_row.append( cluster.ehad3() )

      # Fill the event
      self.fill(event_row)

    return StatusCode.SUCCESS
  

  def finalize( self ):

    d = { "features"  : self._event_label ,
          "data"      : np.array( self._event )
          }

    from Gaugi import save
    save( d, self._outputname, protocol = 'savez_compressed')
    return StatusCode.SUCCESS












