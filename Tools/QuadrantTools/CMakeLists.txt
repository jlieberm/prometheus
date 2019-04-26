################################################################################
# Package: prometheus
################################################################################

if($ENV{Athena_SET_UP})
  # Declare the package name:
  atlas_subdir( QuadrantTools )
  # Install files from the package:
  atlas_install_python_modules( python/*.py )
endif()
