################################################################################
# Package: prometheus
################################################################################

if($ENV{Athena_SETUP} STREQUAL "on")
  # Declare the package name:
  atlas_subdir( prometheus )
  # Install files from the package:
  #atlas_install_python_modules( python/*.py python/storage/ python/messenger/  python/mainloop/ )
  atlas_install_python_modules( python/* )
  atlas_install_joboptions( share/*.py )
else()

  gaugi_install_python_modules( ${CMAKE_CURRENT_SOURCE_DIR}/python prometheus)

endif()
