################################################################################
# Package: prometheus
################################################################################


#include_directories(${CMAKE_SOURCE_DIR} ${ROOT_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})
#
#file(GLOB_RECURSE HEADERS EventAtlas/*)
#
#ROOT_GENERATE_DICTIONARY(EventAtlasDict ${HEADERS}
#                                        LINKDEF
#                                        ${CMAKE_CURRENT_SOURCE_DIR}/src/LinkDef.h
#                                        MODULE
#                                        EventAtlas)
#
#add_library(EventAtlas  OBJECT EventAtlasDict.cxx)
#install(FILES ${HEADERS}  DESTINATION EventAtlas)

prometheus_install_python_modules( ${CMAKE_CURRENT_SOURCE_DIR}/python EventAtlas)


