################################################################################
# Package: prometheus
################################################################################

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


