################################################################################
# Package: RingerSelectorTools
################################################################################

if($ENV{Athena_SET_UP})
  # Declare the package name:
  atlas_subdir( RingerSelectorTools )
  
  # Declare the package's dependencies:
  atlas_depends_on_subdirs( PUBLIC
                            PathResolver
                            PRIVATE
                            #${extra_dep}
                            )
  
  # External dependencies:
  find_package( ROOT COMPONENTS Core Hist Tree RIO Hist )
  
  atlas_add_root_dictionary( RingerSelectorTools RingerSelectorToolsDictSource
                            ROOT_HEADERS RingerSelectorTools/*.h Root/LinkDef.h
                            EXTERNAL_PACKAGES ROOT
  )
  
  #Then we can proceed to a full installation:
  atlas_add_library( RingerSelectorTools
    Root/*.cxx Root/tools/*.cxx Root/tools/procedures/*.cxx Root/tools/common/*.cxx 
      ${RingerSelectorToolsDictSource}
      PUBLIC_HEADERS RingerSelectorTools
      INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
      LINK_LIBRARIES ${ROOT_LIBRARIES} PathResolver
    )
  
  # Install files from the package:
  atlas_install_python_modules( python/*.py  )

else()

  include_directories(${CMAKE_SOURCE_DIR} ${ROOT_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR})
  include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../Tools/PathResolver)
  include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../Gaugi)
  
  file(GLOB_RECURSE HEADERS RingerSelectorTools/*)
  file(GLOB_RECURSE SOURCES Root/*.cxx Root/tools/*)  
  ROOT_GENERATE_DICTIONARY(RingerSelectorToolsDict ${HEADERS}
                                          LINKDEF
                                          ${CMAKE_CURRENT_SOURCE_DIR}/Root/LinkDef.h
                                          MODULE
                                          RingerSelectorTools)
  add_library(RingerSelectorTools  OBJECT ${SOURCES} RingerSelectorToolsDict.cxx)
  install(FILES ${HEADERS}  DESTINATION RingerSelectorTools)



endif()

