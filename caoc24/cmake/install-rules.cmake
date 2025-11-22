install(
    TARGETS caoc24_exe
    RUNTIME COMPONENT caoc24_Runtime
)

if(PROJECT_IS_TOP_LEVEL)
  include(CPack)
endif()
