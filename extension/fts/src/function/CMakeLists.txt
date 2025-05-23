add_library(fts_function
        STATIC
        fts_config.cpp
        fts_index_utils.cpp
        query_fts_bind_data.cpp
        stem.cpp
        )

target_include_directories(fts_function PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/../include)
