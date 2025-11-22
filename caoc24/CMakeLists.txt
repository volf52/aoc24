cmake_minimum_required(VERSION 3.21)

include(cmake/prelude.cmake)

project(
    caoc24
    VERSION 0.1.0
    DESCRIPTION "AOC 2024"
    HOMEPAGE_URL "https://example.com/"
    LANGUAGES C
)

include(cmake/variables.cmake)

# ---- Declare library ----

add_library(
    caoc24_lib OBJECT
    src/lib.c
)

target_include_directories(
    caoc24_lib ${warning_guard}
    PUBLIC
    "\$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/src>"
)

target_compile_features(caoc24_lib PUBLIC c_std_99)

# ---- Declare executable ----

add_executable(caoc24_exe src/main.c)
add_executable(caoc24::exe ALIAS caoc24_exe)

set_property(TARGET caoc24_exe PROPERTY OUTPUT_NAME caoc24)

target_compile_features(caoc24_exe PRIVATE c_std_99)

target_link_libraries(caoc24_exe PRIVATE caoc24_lib)

# ---- Install rules ----

if(NOT CMAKE_SKIP_INSTALL_RULES)
  include(cmake/install-rules.cmake)
endif()

# ---- Developer mode ----

if(NOT caoc24_DEVELOPER_MODE)
  return()
elseif(NOT PROJECT_IS_TOP_LEVEL)
  message(
      AUTHOR_WARNING
      "Developer mode is intended for developers of caoc24"
  )
endif()

include(cmake/dev-mode.cmake)
