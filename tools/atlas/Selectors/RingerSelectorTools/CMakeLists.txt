################################################################################
# Package: RingerSelectorTools
################################################################################


include_directories(${CMAKE_SOURCE_DIR} ${ROOT_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../PathResolver)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../../../Gaugi)

file(GLOB_RECURSE HEADERS RingerSelectorTools/*)
file(GLOB_RECURSE SOURCES Root/*.cxx Root/tools/*)  
ROOT_GENERATE_DICTIONARY(RingerSelectorToolsDict ${HEADERS}
                                        LINKDEF
                                        ${CMAKE_CURRENT_SOURCE_DIR}/Root/LinkDef.h
                                        MODULE
                                        RingerSelectorTools)
add_library(RingerSelectorTools  OBJECT ${SOURCES} RingerSelectorToolsDict.cxx)
install(FILES ${HEADERS}  DESTINATION RingerSelectorTools)

gaugi_install_python_modules( ${CMAKE_CURRENT_SOURCE_DIR}/python RingerSelectorTools)



