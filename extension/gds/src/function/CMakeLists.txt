add_subdirectory(config)

add_library(gds_function
        STATIC
        component_ids.cpp
        )

target_include_directories(gds_function PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/../include)
