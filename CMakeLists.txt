

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
add_subdirectory(tools/event_dump)
add_subdirectory(tools/event_selection)
add_subdirectory(tools/efficiency)
add_subdirectory(tools/profiles)
add_subdirectory(tools/quadrant)
add_subdirectory(tools/impact)
add_subdirectory(trigger)
add_subdirectory(events)




