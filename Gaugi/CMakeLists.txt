################################################################################
# Package: prometheus
################################################################################

# Declare the package name:
atlas_subdir( Gaugi )

if( XAOD_STANDALONE )
  # We don't install rDev on GRID if we are on XAOD_STANDALONE mode
  if( NOT DEFINED $ENV{PanDA_TaskID} )
    # Declare the package's dependencies:
    atlas_depends_on_subdirs( PUBLIC
                              AsgTools
                              PathResolver
                              PATCore
                              PRIVATE
                              #${extra_dep}
                              )

    # External dependencies:
		find_package( ROOT COMPONENTS Core Hist Tree RIO Hist )

    atlas_add_root_dictionary( Gaugi GaugiDictSource
                              ROOT_HEADERS Gaugi/*.h Root/LinkDef.h
                              EXTERNAL_PACKAGES ROOT
    )
  # Then we can proceed to a full installation:
      atlas_add_library( prometheus
        Root/*.cxx Root/*.cxx Root/*.cxx ${GaugiDictSource}
                         PUBLIC_HEADERS Gaugi
                         INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
                         LINK_LIBRARIES ${ROOT_LIBRARIES} AsgTools PathResolver PATCoreLib
                       )
  endif()
endif()

# Install files from the package:
atlas_install_python_modules( python/*.py python/storage python/messenger python/mainloop )


