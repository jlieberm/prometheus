

function(prometheus_initialize)
  file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/python)
  file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
  file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/scripts)
endfunction(prometheus_initialize)


function(prometheus_install_python_modules filepath module)
  message(STATUS "${filepath} -> ${CMAKE_BINARY_DIR}/python/${module}")
    execute_process(COMMAND ${CMAKE_COMMAND} -E create_symlink ${filepath} ${CMAKE_BINARY_DIR}/python/${module})
endfunction(prometheus_install_python_modules)


function(prometheus_install_scripts filepath)

  file(GLOB SCRIPTS ${filepath}/*)
  FOREACH( SCRIPT ${SCRIPTS})
    get_filename_component(sname ${SCRIPT} NAME)
    message(STATUS "${SCRIPT} -> ${CMAKE_BINARY_DIR}/scripts/${sname}")
    execute_process(COMMAND ${CMAKE_COMMAND} -E create_symlink ${SCRIPT} ${CMAKE_BINARY_DIR}/scripts/${sname})
  ENDFOREACH()

endfunction(prometheus_install_scripts)




function( prometheus_finalize )

  file(GLOB SO_FILES ${CMAKE_BINARY_DIR}/*.so)
  FOREACH( SFILE ${SO_FILES})
    execute_process(POST_BUILD COMMAND ${CMAKE_COMMAND} -E create_symlink ${SFILE} ${CMAKE_BINARY_DIR}/lib/)
  ENDFOREACH()

endfunction( prometheus_finalize )
