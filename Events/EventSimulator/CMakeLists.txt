################################################################################
# Package: prometheus
################################################################################

# Declare the package name:
atlas_subdir( EventSimulator )

if( XAOD_STANDALONE )
  # Declare the package's dependencies:
  atlas_depends_on_subdirs( PUBLIC
                            Gaugi
                            EventCommon
                            PRIVATE
                            #${extra_dep}
                            )

  # External dependencies:
	find_package( ROOT COMPONENTS Core Hist Tree RIO Hist )

  atlas_add_root_dictionary( EventSimulator EventSimulatorDictSource
    ROOT_HEADERS EventSimulator/*.h Root/LinkDef.h
    EXTERNAL_PACKAGES ROOT
  )
  # Then we can proceed to a full installation:
  atlas_add_library( EventSimulator
    Root/*.h  ${EventSimulatorDictSource}
    PUBLIC_HEADERS EventSimulator
    INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
    LINK_LIBRARIES ${ROOT_LIBRARIES}
  )
endif()

# Install files from the package:
atlas_install_python_modules( python/*.py )


