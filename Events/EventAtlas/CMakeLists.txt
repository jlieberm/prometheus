################################################################################
# Package: prometheus
################################################################################


include_directories(${CMAKE_SOURCE_DIR} ${ROOT_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})

file(GLOB_RECURSE HEADERS EventAtlas/*)

ROOT_GENERATE_DICTIONARY(EventAtlasDict ${HEADERS}
                                        LINKDEF
                                        ${CMAKE_CURRENT_SOURCE_DIR}/Root/LinkDef.h
                                        MODULE
                                        EventAtlas)
                                 
add_library(EventAtlas  OBJECT EventAtlasDict.cxx)
install(FILES ${HEADERS}  DESTINATION EventAtlas)

gaugi_install_python_modules( ${CMAKE_CURRENT_SOURCE_DIR}/python EventAtlas)


