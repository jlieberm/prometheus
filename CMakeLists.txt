

cmake_minimum_required(VERSION 3.0)


project(prometheus)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -DDROP_CGAL")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include(core/cmake/InstallPrometheusFunctions.cmake)

prometheus_initialize()

find_package( PythonInterp REQUIRED)
find_package( PythonLibs REQUIRED)


add_subdirectory(core)
add_subdirectory(analysis/CollectorTool)
add_subdirectory(analysis/EventSelectionTool)
add_subdirectory(analysis/EfficiencyTools)
add_subdirectory(analysis/PileupCorrectionTools)
add_subdirectory(analysis/ProfileTools)
add_subdirectory(analysis/QuadrantTools)
add_subdirectory(analysis/ImpactTools)
add_subdirectory(trigger)
add_subdirectory(events)




