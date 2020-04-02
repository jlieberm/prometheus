

cmake_minimum_required(VERSION 3.0)


project(prometheus)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -DDROP_CGAL")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# mare ROOT dependenc
find_package(ROOT COMPONENTS EG Eve Geom Gui GuiHtml GenVector Hist Physics Matrix Graf RIO Tree Gpad RGL MathCore)
include(${ROOT_USE_FILE})
include(external/gaugi/cmake/InstallGaugiFunctions.cmake)

gaugi_initialize()

#set( Python_ADDITIONAL_VERSIONS 3.0)
find_package( PythonInterp REQUIRED)
find_package( PythonLibs REQUIRED)
find_package( Boost COMPONENTS python system filesystem)
include_directories( ${Boost_INCLUDE_DIR} )
link_directories( ${Boost_LIBRARY_DIR} )

### If needed to find numpy check caffe script
### https://github.com/PMBio/peer/blob/master/cmake/FindNumpy.cmake
if (NOT NUMPY_INCLUDE_DIR)
    exec_program ("${PYTHON_EXECUTABLE}"
        ARGS "-c 'import numpy; print(numpy.get_include())'"
      OUTPUT_VARIABLE NUMPY_INCLUDE_DIR
      RETURN_VALUE NUMPY_NOT_FOUND)
    if (NUMPY_INCLUDE_DIR MATCHES "Traceback")
    # Did not successfully include numpy
      set(NUMPY_FOUND FALSE)
    else (NUMPY_INCLUDE_DIR MATCHES "Traceback")
    # successful
      set (NUMPY_FOUND TRUE)
      set (NUMPY_INCLUDE_DIR ${NUMPY_INCLUDE_DIR} CACHE PATH "Numpy include path")
    endif (NUMPY_INCLUDE_DIR MATCHES "Traceback")
    if (NUMPY_FOUND)
      if (NOT NUMPY_FIND_QUIETLY)
        message (STATUS "Numpy headers found")
      endif (NOT NUMPY_FIND_QUIETLY)
    else (NUMPY_FOUND)
      if (NUMPY_FIND_REQUIRED)
        message (FATAL_ERROR "Numpy headers missing")
      endif (NUMPY_FIND_REQUIRED)
    endif (NUMPY_FOUND)
    mark_as_advanced (NUMPY_INCLUDE_DIR)
endif (NOT NUMPY_INCLUDE_DIR)



include_directories(${NUMPY_INCLUDE_DIR})


if(NUMPY_FOUND)
  message(STATUS "NumPy ver. ${NUMPY_VERSION} found (include: ${NUMPY_INCLUDE_DIR})")
endif()




add_subdirectory(external/gaugi)
add_subdirectory(prometheus)
add_subdirectory(tools/atlas/CommonTools)
add_subdirectory(tools/atlas/CollectorTool)
add_subdirectory(tools/atlas/EfficiencyTools)
add_subdirectory(tools/atlas/EmulationTools)
add_subdirectory(tools/atlas/EventSelectionTool)
add_subdirectory(tools/atlas/PathResolver)
add_subdirectory(tools/atlas/PileupCorrectionTools)
add_subdirectory(tools/atlas/ProfileTools)
add_subdirectory(tools/atlas/QuadrantTools)
add_subdirectory(tools/atlas/Selectors/RingerSelectorTools)
add_subdirectory(tools/atlas/Selectors/TrigEgammaL2CaloSelectorTool)
add_subdirectory(tools/simulator/SimValidationTools)
add_subdirectory(events/EventAtlas)
#add_subdirectory(events/EventSimulator)
add_subdirectory(external/monet)
add_subdirectory(external/pytex)

# check if GEANT4 is in the path
#if( $ENV{G4_SETUP} STREQUAL "on")
#  message (STATUS "Geant is found")
#  add_subdirectory(Simulator)
#endif()



add_library(prometheus SHARED
  $<TARGET_OBJECTS:EventAtlas>
  #$<TARGET_OBJECTS:EventSimulator>
  $<TARGET_OBJECTS:PathResolver>
  $<TARGET_OBJECTS:RingerSelectorTools>
)


target_link_Libraries(prometheus ${ROOT_LIBRARIES} ${ROOT_COMPONENT_LIBRARIES} ${Boost_PYTHON_LIBRARIES} ${PYTHON_LIBRARIES} 
  ${Boost_FILESYSTEM_LIBRARY} ${Boost_SYSTEM_LIBRARY})


