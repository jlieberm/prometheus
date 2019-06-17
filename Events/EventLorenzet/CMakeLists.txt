################################################################################
# Package: prometheus
################################################################################

if($ENV{Athena_SETUP} STREQUAL "on")
  # Declare the package name:
  atlas_subdir( EventLorenzet )
  
  # Declare the package's dependencies:
  atlas_depends_on_subdirs( PUBLIC
                            #EventCommon
                            PRIVATE
                            #${extra_dep}
                            )
  
  # External dependencies:
  find_package( ROOT COMPONENTS Core Hist Tree RIO Hist )
  
  atlas_add_root_dictionary( 
    EventLorenzetLib 
    EventLorenzetCintDict
    ROOT_HEADERS 
    EventLorenzet/*.h 
    Root/LinkDef.h
    EXTERNAL_PACKAGES ROOT
  )
  
  # Then we can proceed to a full installation:
  atlas_add_library( 
    EventLorenzetLib
    EventLorenzet/*.h
    ${EventGeantCintDict}
    PUBLIC_HEADERS  EventGeant
    INCLUDE_DIRS    ${ROOT_INCLUDE_DIRS}
    LINK_LIBRARIES  ${ROOT_LIBRARIES}
  )
  
  # Install files from the package:
  atlas_install_python_modules( python/*.py )
else()


  include_directories(${CMAKE_SOURCE_DIR} ${ROOT_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})
  file(GLOB_RECURSE HEADERS EventLorenzet/*)
  
  ROOT_GENERATE_DICTIONARY(EventLorenzetDict ${HEADERS}
                                          LINKDEF
                                          ${CMAKE_CURRENT_SOURCE_DIR}/Root/LinkDef.h
                                          MODULE
                                          EventLorenzet)
                                        
                                        add_library(EventLorenzet  OBJECT EventLorenzetDict.cxx)
  install(FILES ${HEADERS}  DESTINATION EventLorenzet)

  gaugi_install_python_modules( ${CMAKE_CURRENT_SOURCE_DIR}/python EventLorenzet)



endif()

