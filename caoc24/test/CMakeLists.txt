# Parent project does not export its library target, so this CML implicitly
# depends on being added from it, i.e. the testing is done only from the build
# tree and is not feasible from an install location

project(caoc24Tests LANGUAGES C)

# ---- Tests ----

add_executable(caoc24_test source/caoc24_test.c)
target_link_libraries(caoc24_test PRIVATE caoc24_lib)
target_compile_features(caoc24_test PRIVATE c_std_99)

add_test(NAME caoc24_test COMMAND caoc24_test)

# ---- End-of-file commands ----

add_folders(Test)
