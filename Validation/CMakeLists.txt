################################################################################
# Package: prometheus
################################################################################

# Declare the package name:
atlas_subdir( Validation )
# Install files from the package:


atlas_install_scripts( test/*.sh )
atlas_install_joboptions( share/*.py )


file( MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/unitTestRun_gaugiAtlas )
atlas_add_test( gaugiAtlas
   SCRIPT test/test_gaugi_atlas.sh
   PROPERTIES TIMEOUT 1000   
   PROPERTIES WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/unitTestRun_gaugiAtlas
)




