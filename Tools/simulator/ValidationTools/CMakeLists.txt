################################################################################
# Package: prometheus
################################################################################

if($ENV{Athena_SETUP} STREQUAL "on")
  # Declare the package name:
  atlas_subdir( LorenzetTools )
  # Install files from the package:
  atlas_install_python_modules( python/*.py )
  atlas_install_scripts( scripts/*.py )
else()
  gaugi_install_python_modules( ${CMAKE_CURRENT_SOURCE_DIR}/python LorenzetTools)
endif()
