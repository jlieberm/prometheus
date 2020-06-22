

cmake_minimum_required(VERSION 3.0)


project(prometheus)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -DDROP_CGAL")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# mare ROOT dependenc
find_package(ROOT COMPONENTS EG Eve Geom Gui GuiHtml GenVector Hist Physics Matrix Graf RIO Tree Gpad RGL MathCore)
include(${ROOT_USE_FILE})
include(core/prometheus/cmake/InstallPrometheusFunctions.cmake)

prometheus_initialize()

#set( Python_ADDITIONAL_VERSIONS 3.0)
find_package( PythonInterp REQUIRED)
find_package( PythonLibs REQUIRED)
#find_package( Boost COMPONENTS python system filesystem)
#include_directories( ${Boost_INCLUDE_DIR} )
#link_directories( ${Boost_LIBRARY_DIR} )



add_subdirectory(core/prometheus)
add_subdirectory(tools/CommonTools)
add_subdirectory(tools/CollectorTool)
add_subdirectory(tools/EfficiencyTools)
add_subdirectory(tools/EmulationTools)
add_subdirectory(tools/EventSelectionTool)
#add_subdirectory(tools/PathResolver)
add_subdirectory(tools/PileupCorrectionTools)
add_subdirectory(tools/ProfileTools)
add_subdirectory(tools/QuadrantTools)
add_subdirectory(tools/Selectors/RingerSelectorTools)
add_subdirectory(tools/Selectors/TrigEgammaL2CaloSelectorTool)
add_subdirectory(events)


add_library(prometheus SHARED
  $<TARGET_OBJECTS:EventAtlas>
)


#target_link_Libraries(prometheus ${ROOT_LIBRARIES} ${ROOT_COMPONENT_LIBRARIES} ${Boost_PYTHON_LIBRARIES} ${PYTHON_LIBRARIES} 
#  ${Boost_FILESYSTEM_LIBRARY} ${Boost_SYSTEM_LIBRARY})

target_link_Libraries(prometheus ${ROOT_LIBRARIES} ${ROOT_COMPONENT_LIBRARIES} ${PYTHON_LIBRARIES} )


