################################################################################
# Package: prometheus
################################################################################

if($ENV{Athena_SET_UP})
  # Declare the package name:
  atlas_subdir( PileupCorrectionTools )
  # Install files from the package:
  atlas_install_python_modules( python/*.py )
else()
  gaugi_install_python_modules( ${CMAKE_CURRENT_SOURCE_DIR}/python PileCorrectionTools)
endif()
