cmake_minimum_required(VERSION 2.8)

PROJECT(venus_engine)

MESSAGE (STATUS "Start cmake " ${PROJECT_NAME})

SET(PROJECT_STATIC
venus_engine_static
)

INCLUDE_DIRECTORIES(
inc
${VENUS_ENGINE_SOURCE}/include
${VENUS_ENGINE_SOURCE}/libs/third_lib/inc
${VENUS_ENGINE_SOURCE}/libs/venus_engine/src/logger
${VENUS_ENGINE_SOURCE}/libs/venus_engine/src/demo_lib
)

AUX_SOURCE_DIRECTORY(src DIR_SRCS)
AUX_SOURCE_DIRECTORY(src/logger DIR_SRCS)
AUX_SOURCE_DIRECTORY(src/demo_lib DIR_SRCS)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -g -Wall -Wfatal-errors -Wextra -Wshadow -Wpointer-arith  -Werror -Wcast-qual -Winline -Wunreachable-code -Wcast-align -Wundef -Wredundant-decls")
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wchar-subscripts -Wcomment -Wmissing-braces -Wparentheses -Wsequence-point  -Wmaybe-uninitialized -Wfloat-equal -Wreturn-type -Wsign-compare -Wconversion-null -Wsizeof-pointer-memaccess -Wreorder -Woverflow")
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O -fPIE -pipe -fstack-protector -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE -D_LARGE_FILE_SOURCE ")
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wformat-security -pedantic -Wunused-but-set-parameter  -Wunused-but-set-variable -Wunused-function -Wunused-label -Wunused-variable")
#SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Waggregate-return)
#SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wl,-z,relro")
#SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pedantic-errors")

#SET(CMAKE_C_FLAGS "${CMAKE_CXX_FLAGS} -g2 -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE -D_LARGE_FILE_SOURCE ")

LINK_DIRECTORIES(${VENUS_ENGINE_SOURCE}/libs/third_lib/lib/log4cplus)

ADD_LIBRARY( ${PROJECT_NAME} SHARED ${DIR_SRCS})
SET_TARGET_PROPERTIES (${PROJECT_NAME} PROPERTIES VERSION 1.0.0 SOVERSION 1)

#ADD_LIBRARY(${PROJECT_STATIC} STATIC ${DIR_SRCS})
#SET_TARGET_PROPERTIES (${PROJECT_STATIC} PROPERTIES OUTPUT_NAME ${PROJECT_NAME})

TARGET_LINK_LIBRARIES(${PROJECT_NAME} log4cplus pthread)

#GET_TARGET_PROPERTY (OUTPUT_VALUE ${PROJECT_STATIC} OUTPUT_NAME)
#MESSAGE (STATUS "This is the hello_static OUTPUT_NAME: " ${OUTPUT_VALUE})

#INSTALL (FILES module.h DESTINATION include/obj)
INSTALL(TARGETS ${PROJECT_NAME} 
	LIBRARY DESTINATION lib64)
#	ARCHIVE DESTINATION lib64)

	
