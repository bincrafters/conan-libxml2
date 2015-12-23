project(bzip2)
cmake_minimum_required(VERSION 2.8)
include(../conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

if(MSVC OR MSVC90 OR MSVC10)
  set(MSVC ON)
endif (MSVC OR MSVC90 OR MSVC10)

set(bzip2_STAT_SRCS blocksort.c  bzlib.c compress.c  crctable.c  decompress.c  huffman.c randtable.c  unzcrash.c)

add_library(bz2 ${bzip2_STAT_SRCS})
add_executable(bzip2 bzip2.c)
target_link_libraries(bzip2 bz2)

