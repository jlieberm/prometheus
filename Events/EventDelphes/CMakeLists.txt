################################################################################
# Package: prometheus
################################################################################

if($ENV{Athena_SETUP} STREQUAL "on")
  # Declare the package name:
  atlas_subdir( EventDelphes )
  
  # Declare the package's dependencies:
  atlas_depends_on_subdirs( PUBLIC
                            #EventCommon
                            PRIVATE
                            #${extra_dep}
                            )
  
  # External dependencies:
  find_package( ROOT COMPONENTS Core Hist Tree RIO Hist )
  
  atlas_add_root_dictionary( 
    EventDelphesLib 
    EventDelphesCintDict
    ROOT_HEADERS 
    EventDelphes/*.h 
    Root/LinkDef.h
    EXTERNAL_PACKAGES ROOT
  )
  
  # Then we can proceed to a full installation:
  atlas_add_library( 
    EventDelphesLib
    EventDelphes/*.h
    ${EventDelphesCintDict}
    PUBLIC_HEADERS  EventDelphes
    INCLUDE_DIRS    ${ROOT_INCLUDE_DIRS}
    LINK_LIBRARIES  ${ROOT_LIBRARIES}
  )
  
  # Install files from the package:
  atlas_install_python_modules( python/*.py )

else()

  include_directories(${CMAKE_SOURCE_DIR} ${ROOT_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})
  file(GLOB_RECURSE HEADERS EventDelphes/*)
  
  ROOT_GENERATE_DICTIONARY(EventDelphesDict ${HEADERS}
                                          LINKDEF
                                          ${CMAKE_CURRENT_SOURCE_DIR}/Root/LinkDef.h
                                          MODULE
                                          EventDelphes)
                                        
  add_library(EventDelphes  OBJECT EventDelphesDict.cxx)
  install(FILES ${HEADERS}  DESTINATION EventDelphes)

  gaugi_install_python_modules( ${CMAKE_CURRENT_SOURCE_DIR}/python EventDelphes)


endif()
