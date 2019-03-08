################################################################################
# Package: RingerSelectorTools
################################################################################

# Declare the package name:
atlas_subdir( RingerSelectorTools )

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

atlas_add_root_dictionary( RingerSelectorTools RingerSelectorToolsDictSource
                          ROOT_HEADERS RingerSelectorTools/*.h
                          EXTERNAL_PACKAGES ROOT
)

#Then we can proceed to a full installation:
atlas_add_library( RingerSelectorTools
    Root/*.cxx Root/tools/*.cxx Root/tools/procedures/*.cxx Root/tools/common/*.cxx 
    ${RingerSelectorToolsDictSource}
    PUBLIC_HEADERS RingerSelectorTools
    INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
    LINK_LIBRARIES ${ROOT_LIBRARIES} AsgTools PathResolver PATCoreLib
  )

# Install files from the package:
atlas_install_python_modules( python/*.py  )


