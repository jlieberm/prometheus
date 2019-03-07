################################################################################
# Package: prometheus
################################################################################

# Declare the package name:
atlas_subdir( Gaugi )
# Install files from the package:
atlas_install_python_modules( python/*.py python/storage python/messenger python/mainloop )

atlas_install_joboptions( share/*.py )
