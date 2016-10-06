PROJECT(MyHello)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(example example.c)

find_package(ZLIB)
find_package(LibXml2)

if(LIBXML2_FOUND AND ZLIB_FOUND)
    include_directories(${LIBXML2_INCLUDE_DIRS})
    include_directories(${ZLIB_INCLUDE_DIRS})
    target_link_libraries(example ${LIBXML2_LIBRARIES} ${ZLIB_LIBRARIES})
    if(UNIX)
       target_link_libraries(example ${LIBXML2_LIBRARIES} ${ZLIB_LIBRARIES} m) 
    endif()
else()
    message(FATAL_ERROR "Not found libxml2")
endif()


