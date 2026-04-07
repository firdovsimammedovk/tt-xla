# Prefer the active virtualenv's Python so `pip install -r docs/requirements.txt`
# in .venv is the same interpreter Sphinx runs under. (Plain find_package(Python3)
# often picks Homebrew/system Python on macOS and misses venv-installed Sphinx.)
if(DEFINED ENV{VIRTUAL_ENV})
  if(EXISTS "$ENV{VIRTUAL_ENV}/bin/python3")
    set(Python3_EXECUTABLE "$ENV{VIRTUAL_ENV}/bin/python3" CACHE FILEPATH "Python for Sphinx docs" FORCE)
  elseif(EXISTS "$ENV{VIRTUAL_ENV}/bin/python")
    set(Python3_EXECUTABLE "$ENV{VIRTUAL_ENV}/bin/python" CACHE FILEPATH "Python for Sphinx docs" FORCE)
  elseif(EXISTS "$ENV{VIRTUAL_ENV}/Scripts/python.exe")
    set(Python3_EXECUTABLE "$ENV{VIRTUAL_ENV}/Scripts/python.exe" CACHE FILEPATH "Python for Sphinx docs" FORCE)
  endif()
else()
  # No active venv in environment (e.g. CMake from an IDE); use a repo-local env if present.
  if(EXISTS "${CMAKE_SOURCE_DIR}/.venv/bin/python3")
    set(Python3_EXECUTABLE "${CMAKE_SOURCE_DIR}/.venv/bin/python3" CACHE FILEPATH "Python for Sphinx docs" FORCE)
  elseif(EXISTS "${CMAKE_SOURCE_DIR}/venv/bin/python3")
    set(Python3_EXECUTABLE "${CMAKE_SOURCE_DIR}/venv/bin/python3" CACHE FILEPATH "Python for Sphinx docs" FORCE)
  endif()
endif()
set(Python3_FIND_VIRTUALENV FIRST)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

add_custom_target(copy-docs-dir
  COMMAND
    ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}
)

add_custom_target(docs
  COMMAND
    ${Python3_EXECUTABLE} -m sphinx.cmd.build
    -b html
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}/book
  COMMENT "Building Sphinx HTML documentation (output: build/docs/book)"
)

find_package(Doxygen)

if (DOXYGEN_FOUND)

  if (NOT EXISTS ${CMAKE_CURRENT_BINARY_DIR}/book/doxygen)
    file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/book/doxygen)
  endif()

  set(DOXYGEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/book/doxygen)
  set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/..)

  add_custom_target(doxygen
    COMMAND
      ${CMAKE_COMMAND} -E make_directory ${DOXYGEN_DIR}
    COMMAND
      ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_SOURCE_DIR}/../cmake/ConfigureDoxygen.cmake
    COMMAND
      doxygen ${DOXYGEN_DIR}/doxygen.cfg
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    DEPENDS
      copy-docs-dir
  )
else()
  message("Doxygen is required to build documentation")
endif()
