
if($ENV{Athena_SETUP} STREQUAL "on")
  message(STATUS "This package is default in athena envs. Dont need to be installed.")

else()
  include_directories(${CMAKE_SOURCE_DIR} ${ROOT_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR} )
  include_directories(${NUMPY_INCLUDE_DIR})
  include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../Gaugi )
  
  if( Boost_PYTHON_FOUND AND PYTHONLIBS_FOUND )
    file(GLOB_RECURSE HEADERS PathResolver/*)
    file(GLOB_RECURSE SOURCES Root/*.cxx)
    
    ROOT_GENERATE_DICTIONARY(PathResolverDict  ${HEADERS}
                                              LINKDEF
                                              Root/LinkDef.h
                                              MODULE
                                              PathResolver
                                              )
    #Create the CustomClasses library with the ROOT dictionary.
    add_library(PathResolver OBJECT  ${SOURCES} PathResolverDict.cxx)
  endif()
  
endif()


