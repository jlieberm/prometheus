
include_directories(${CMAKE_SOURCE_DIR} ${ROOT_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR} )
include_directories(${NUMPY_INCLUDE_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../../Gaugi)

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
#install(FILES ${HEADERS}  DESTINATION PathResolver)
  
gaugi_install_python_modules( ${CMAKE_CURRENT_SOURCE_DIR}/python PathResolver)


