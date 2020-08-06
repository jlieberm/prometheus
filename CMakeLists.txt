

cmake_minimum_required(VERSION 3.0)


project(prometheus)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -DDROP_CGAL")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include(core/prometheus/cmake/InstallPrometheusFunctions.cmake)

prometheus_initialize()

find_package( PythonInterp REQUIRED)
find_package( PythonLibs REQUIRED)


add_subdirectory(core/prometheus)
add_subdirectory(tools/analysis/CollectorTool)
add_subdirectory(tools/analysis/EventSelectionTool)
add_subdirectory(tools/analysis/EfficiencyTools)
add_subdirectory(tools/analysis/PileupCorrectionTools)
add_subdirectory(tools/analysis/ProfileTools)
add_subdirectory(tools/analysis/QuadrantTools)
add_subdirectory(tools/analysis/ImpactTools)
add_subdirectory(tools/trigger/RingerSelectorTools)
add_subdirectory(tools/trigger/TrigEgammaEmulationTool)
add_subdirectory(events)




