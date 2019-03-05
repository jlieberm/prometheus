################################################################################
# Package: prometheus
################################################################################

# Declare the package name:
atlas_subdir( EventAtlas )

# Declare the package's dependencies:
atlas_depends_on_subdirs( PUBLIC
                          #EventCommon
                          PRIVATE
                          #${extra_dep}
                          )

# External dependencies:
find_package( ROOT COMPONENTS Core Hist Tree RIO Hist )

atlas_add_root_dictionary( 
  EventAtlasLib 
  EventAtlasCintDict
  ROOT_HEADERS 
  EventAtlas/*.h 
  Root/LinkDef.h
  EXTERNAL_PACKAGES ROOT
)

# Then we can proceed to a full installation:
atlas_add_library( 
  EventAtlasLib
  EventAtlas/*.h
  ${EventAtlasCintDict}
  PUBLIC_HEADERS  EventAtlas
  INCLUDE_DIRS    ${ROOT_INCLUDE_DIRS}
  LINK_LIBRARIES  ${ROOT_LIBRARIES}
)

# Install files from the package:
atlas_install_python_modules( python/*.py )


