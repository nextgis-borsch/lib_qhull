################################################################################
# Project:  Lib QHull
# Purpose:  CMake build scripts
# Author:   Dmitry Baryshnikov, dmitry.baryshnikov@nexgis.com
################################################################################
# Copyright (C) 2017, NextGIS <info@nextgis.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
################################################################################

cmake_minimum_required(VERSION 2.8.12 FATAL_ERROR)

project(qhull)

# Some init settings
set(CMAKE_COLOR_MAKEFILE ON)
# Set path to additional CMake modules
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

if(OSX_FRAMEWORK AND (BUILD_SHARED_LIBS OR BUILD_STATIC_LIBS))
  message(FATAL_ERROR "Only OSX_FRAMEWORK key or any or both BUILD_SHARED_LIBS
                       and BUILD_STATIC_LIBS keys are permitted")
endif()

if(OSX_FRAMEWORK)
  set(INSTALL_BIN_DIR "${CMAKE_INSTALL_PREFIX}/bin" CACHE INTERNAL "Installation directory for executables" FORCE)
  set(INSTALL_LIB_DIR "${CMAKE_INSTALL_PREFIX}/Library/Frameworks" CACHE INTERNAL "Installation directory for libraries" FORCE)
  set(INSTALL_INC_DIR "${INSTALL_LIB_DIR}/${PROJECT_NAME}.framework/Headers" CACHE INTERNAL "Installation directory for headers" FORCE)
  set(SKIP_INSTALL_HEADERS ON)
  set(SKIP_INSTALL_FILES ON)
  set(SKIP_INSTALL_EXPORT ON)
  set(CMAKE_MACOSX_RPATH ON)
  set(SKIP_INSTALL_DOCS ON)
else()
    include(GNUInstallDirs)

    set(INSTALL_BIN_DIR ${CMAKE_INSTALL_FULL_BINDIR} CACHE INTERNAL "Installation directory for executables" FORCE)
    set(INSTALL_LIB_DIR ${CMAKE_INSTALL_FULL_LIBDIR} CACHE INTERNAL "Installation directory for libraries" FORCE)
    set(INSTALL_INC_DIR ${CMAKE_INSTALL_FULL_INCLUDEDIR} CACHE INTERNAL "Installation directory for headers" FORCE)
    set(INSTALL_DOC_DIR ${CMAKE_INSTALL_FULL_DOCDIR} CACHE INTERNAL "Share directory for documents" FORCE)
    set(INSTALL_MAN_DIR ${CMAKE_INSTALL_FULL_MANDIR} CACHE INTERNAL "Share directory for manuals" FORCE)
endif()

if(CMAKE_GENERATOR_TOOLSET MATCHES "v([0-9]+)_xp")
    add_definitions(-D_WIN32_WINNT=0x0501)
endif()

include(util)
check_version(VERSION VERSION2 SOVERSION)

if(OSX_FRAMEWORK)
    set(FRAMEWORK_VERSION "${SOVERSION}")
endif()
report_version(${PROJECT_NAME} ${VERSION} [${VERSION2}])

include(CheckLFS)
option(WITH_LFS "Enable Large File Support" ON)
check_lfs(WITH_LFS)

# ---------------------------------------
# Define library source files and variables
#
# Files for individual targets are defined with the target
# ---------------------------------------

# Order libqhull object files by frequency of execution.  Small files at end.

# Non-reentrant Qhull
set(
    libqhull_HEADERS
        src/libqhull/libqhull.h
        src/libqhull/geom.h
        src/libqhull/io.h
        src/libqhull/mem.h
        src/libqhull/merge.h
        src/libqhull/poly.h
        src/libqhull/qhull_a.h
        src/libqhull/qset.h
        src/libqhull/random.h
        src/libqhull/stat.h
        src/libqhull/user.h
)
set(
    libqhull_SOURCES
        src/libqhull/global.c
        src/libqhull/stat.c
        src/libqhull/geom2.c
        src/libqhull/poly2.c
        src/libqhull/merge.c
        src/libqhull/libqhull.c
        src/libqhull/geom.c
        src/libqhull/poly.c
        src/libqhull/qset.c
        src/libqhull/mem.c
        src/libqhull/random.c
        src/libqhull/usermem.c
        src/libqhull/userprintf.c
        src/libqhull/io.c
        src/libqhull/user.c
        src/libqhull/rboxlib.c
        src/libqhull/userprintf_rbox.c
)

set(
    libqhull_DOC
        src/libqhull/index.htm
        src/libqhull/qh-geom.htm
        src/libqhull/qh-globa.htm
        src/libqhull/qh-io.htm
        src/libqhull/qh-mem.htm
        src/libqhull/qh-merge.htm
        src/libqhull/qh-poly.htm
        src/libqhull/qh-qhull.htm
        src/libqhull/qh-set.htm
        src/libqhull/qh-stat.htm
        src/libqhull/qh-user.htm
        src/libqhull/DEPRECATED.txt
)

set(
    testqset_HEADERS
        src/libqhull/mem.h
        src/libqhull/qset.h
)
set(
    testqset_SOURCES
        src/libqhull/qset.c
        src/libqhull/mem.c
        src/libqhull/usermem.c
        src/testqset/testqset.c
)

# Reeentrant Qhull

set(
    libqhullr_HEADERS
        src/libqhull_r/libqhull_r.h
        src/libqhull_r/geom_r.h
        src/libqhull_r/io_r.h
        src/libqhull_r/mem_r.h
        src/libqhull_r/merge_r.h
        src/libqhull_r/poly_r.h
        src/libqhull_r/qhull_ra.h
        src/libqhull_r/qset_r.h
        src/libqhull_r/random_r.h
        src/libqhull_r/stat_r.h
        src/libqhull_r/user_r.h
)
set(
    libqhullr_SOURCES
        src/libqhull_r/global_r.c
        src/libqhull_r/stat_r.c
        src/libqhull_r/geom2_r.c
        src/libqhull_r/poly2_r.c
        src/libqhull_r/merge_r.c
        src/libqhull_r/libqhull_r.c
        src/libqhull_r/geom_r.c
        src/libqhull_r/poly_r.c
        src/libqhull_r/qset_r.c
        src/libqhull_r/mem_r.c
        src/libqhull_r/random_r.c
        src/libqhull_r/usermem_r.c
        src/libqhull_r/userprintf_r.c
        src/libqhull_r/io_r.c
        src/libqhull_r/user_r.c
        src/libqhull_r/rboxlib_r.c
        src/libqhull_r/userprintf_rbox_r.c
)

set(
    libqhullr_DOC
        src/libqhull_r/index.htm
        src/libqhull_r/qh-geom_r.htm
        src/libqhull_r/qh-globa_r.htm
        src/libqhull_r/qh-io_r.htm
        src/libqhull_r/qh-mem_r.htm
        src/libqhull_r/qh-merge_r.htm
        src/libqhull_r/qh-poly_r.htm
        src/libqhull_r/qh-qhull_r.htm
        src/libqhull_r/qh-set_r.htm
        src/libqhull_r/qh-stat_r.htm
        src/libqhull_r/qh-user_r.htm
)

set(
    testqsetr_HEADERS
        src/libqhull_r/mem_r.h
        src/libqhull_r/qset_r.h
)
set(
    testqsetr_SOURCES
        src/libqhull_r/qset_r.c
        src/libqhull_r/mem_r.c
        src/libqhull_r/usermem_r.c
        src/testqset_r/testqset_r.c
)

# C++ interface to reentrant Qhull

set(
    libqhullcpp_HEADERS
        src/libqhullcpp/Coordinates.h
        src/libqhullcpp/functionObjects.h
        src/libqhullcpp/PointCoordinates.h
        src/libqhullcpp/Qhull.h
        src/libqhullcpp/QhullError.h
        src/libqhullcpp/QhullFacet.h
        src/libqhullcpp/QhullFacetList.h
        src/libqhullcpp/QhullFacetSet.h
        src/libqhullcpp/QhullHyperplane.h
        src/libqhullcpp/QhullIterator.h
        src/libqhullcpp/QhullLinkedList.h
        src/libqhullcpp/QhullPoint.h
        src/libqhullcpp/QhullPoints.h
        src/libqhullcpp/QhullPointSet.h
        src/libqhullcpp/QhullQh.h
        src/libqhullcpp/QhullRidge.h
        src/libqhullcpp/QhullSet.h
        src/libqhullcpp/QhullSets.h
        src/libqhullcpp/QhullStat.h
        src/libqhullcpp/QhullVertex.h
        src/libqhullcpp/QhullVertexSet.h
        src/libqhullcpp/RboxPoints.h
        src/libqhullcpp/RoadError.h
        src/libqhullcpp/RoadLogEvent.h
        src/qhulltest/RoadTest.h
)

set(
    libqhullcpp_SOURCES
        src/libqhullcpp/Coordinates.cpp
        src/libqhullcpp/PointCoordinates.cpp
        src/libqhullcpp/Qhull.cpp
        src/libqhullcpp/QhullFacet.cpp
        src/libqhullcpp/QhullFacetList.cpp
        src/libqhullcpp/QhullFacetSet.cpp
        src/libqhullcpp/QhullHyperplane.cpp
        src/libqhullcpp/QhullPoint.cpp
        src/libqhullcpp/QhullPointSet.cpp
        src/libqhullcpp/QhullPoints.cpp
        src/libqhullcpp/QhullQh.cpp
        src/libqhullcpp/QhullRidge.cpp
        src/libqhullcpp/QhullSet.cpp
        src/libqhullcpp/QhullStat.cpp
        src/libqhullcpp/QhullVertex.cpp
        src/libqhullcpp/QhullVertexSet.cpp
        src/libqhullcpp/RboxPoints.cpp
        src/libqhullcpp/RoadError.cpp
        src/libqhullcpp/RoadLogEvent.cpp
)

# Documentation files (index.htm refers to html/...)

set(
    doc_FILES
        README.txt
        REGISTER.txt
        Announce.txt
        COPYING.txt
        index.htm
)

include_directories(${CMAKE_SOURCE_DIR}/src)

set(LIB_NAME_qhull_CPP qhullcpp)
set(LIB_NAME_qhull libqhull)  # Temporarily avoid name conflict with qhull executable
set(LIB_NAME_qhull_P qhull_p)
set(LIB_NAME_qhull_R qhull_r)


if(BUILD_SHARED_LIBS)
    add_library(${LIB_NAME_qhull} SHARED ${libqhull_SOURCES} ${libqhull_HEADERS}
    src/libqhull/qhull-exports.def)
    set_target_properties (${LIB_NAME_qhull} PROPERTIES
        VERSION ${VERSION}
        SOVERSION ${SOVERSION}
    )
    if(WIN32)
        set_target_properties (${LIB_NAME_qhull} PROPERTIES
            OUTPUT_NAME "qhull"
            IMPORT_SUFFIX "_i.lib"
        )
    endif()
elseif(OSX_FRAMEWORK)
    add_library(${LIB_NAME_qhull} SHARED  ${libqhull_SOURCES} ${libqhull_HEADERS}
    src/libqhull/qhull-exports.def)
    set_target_properties(${LIB_NAME_qhull} PROPERTIES
      FRAMEWORK TRUE
      FRAMEWORK_VERSION ${FRAMEWORK_VERSION}
      MACOSX_FRAMEWORK_SHORT_VERSION_STRING ${VERSION}
      MACOSX_FRAMEWORK_BUNDLE_VERSION ${VERSION}
      MACOSX_FRAMEWORK_IDENTIFIER org.libqhull.libqhull
      XCODE_ATTRIBUTE_INSTALL_PATH "@rpath"
      PUBLIC_HEADER "${libqhull_HEADERS}"
      VERSION ${VERSION}
      SOVERSION ${SOVERSION}
      OUTPUT_NAME "qhull"
      )
else()
    add_library(${LIB_NAME_qhull} STATIC  ${libqhull_SOURCES} ${libqhull_HEADERS})
    if(WIN32)
        set_target_properties (${LIB_NAME_qhull} PROPERTIES
            OUTPUT_NAME "qhull"
        )
    endif()
endif()

if(UNIX)
    target_link_libraries(${LIB_NAME_qhull} m)
endif()

if(BUILD_SHARED_LIBS)
    add_library(${LIB_NAME_qhull_R} SHARED ${libqhullr_SOURCES} ${libqhullr_HEADERS}
    src/libqhull_r/qhull_r-exports.def)
    set_target_properties (${LIB_NAME_qhull_R} PROPERTIES
        VERSION ${VERSION}
        SOVERSION ${SOVERSION}
    )
    if(WIN32)
        set_target_properties(${LIB_NAME_qhull_R} PROPERTIES IMPORT_SUFFIX "_i.lib")
    endif()
elseif(OSX_FRAMEWORK)
    add_library(${LIB_NAME_qhull_R} SHARED  ${libqhullr_SOURCES} ${libqhullr_HEADERS}
    src/libqhull_r/qhull_r-exports.def)
    set_target_properties(${LIB_NAME_qhull_R} PROPERTIES
      FRAMEWORK TRUE
      FRAMEWORK_VERSION ${FRAMEWORK_VERSION}
      MACOSX_FRAMEWORK_SHORT_VERSION_STRING ${VERSION}
      MACOSX_FRAMEWORK_BUNDLE_VERSION ${VERSION}
      MACOSX_FRAMEWORK_IDENTIFIER org.libqhull.libqhullr
      XCODE_ATTRIBUTE_INSTALL_PATH "@rpath"
      PUBLIC_HEADER "${libqhullr_HEADERS}"
      VERSION ${VERSION}
      SOVERSION ${SOVERSION}
      )
else()
    add_library(${LIB_NAME_qhull_R} STATIC  ${libqhullr_SOURCES} ${libqhullr_HEADERS})
endif()

if(UNIX)
    target_link_libraries(${LIB_NAME_qhull_R} m)
endif()

if(BUILD_SHARED_LIBS)
    add_library(${LIB_NAME_qhull_P} SHARED ${libqhull_SOURCES} ${libqhull_HEADERS}
    src/libqhull/qhull_p-exports.def)
    set_target_properties (${LIB_NAME_qhull_P} PROPERTIES
        VERSION ${VERSION}
        SOVERSION ${SOVERSION}
    )
    if(WIN32)
        set_target_properties(${LIB_NAME_qhull_P} PROPERTIES IMPORT_SUFFIX "_i.lib")
    endif()
elseif(OSX_FRAMEWORK)
    add_library(${LIB_NAME_qhull_P} SHARED  ${libqhull_SOURCES} ${libqhull_HEADERS}
    src/libqhull/qhull_p-exports.def)
    set_target_properties(${LIB_NAME_qhull_P} PROPERTIES
      FRAMEWORK TRUE
      FRAMEWORK_VERSION ${FRAMEWORK_VERSION}
      MACOSX_FRAMEWORK_SHORT_VERSION_STRING ${VERSION}
      MACOSX_FRAMEWORK_BUNDLE_VERSION ${VERSION}
      MACOSX_FRAMEWORK_IDENTIFIER org.libqhull.libqhullp
      XCODE_ATTRIBUTE_INSTALL_PATH "@rpath"
      PUBLIC_HEADER "${libqhull_HEADERS}"
      VERSION ${VERSION}
      SOVERSION ${SOVERSION}
      )
else()
    add_library(${LIB_NAME_qhull_P} STATIC  ${libqhull_SOURCES} ${libqhull_HEADERS})
endif()

if(UNIX)
    target_link_libraries(${LIB_NAME_qhull_P} m)
endif()

add_library(${LIB_NAME_qhull_CPP} STATIC  ${libqhullcpp_SOURCES} ${libqhullcpp_HEADERS})
set_target_properties (${LIB_NAME_qhull_CPP} PROPERTIES
    VERSION ${VERSION}
    SOVERSION ${SOVERSION}
)

if(UNIX)
    target_link_libraries(${LIB_NAME_qhull_CPP} m)
endif()

macro(ADD_EXE target sources tll)
    add_executable(${target} ${sources})
    target_link_libraries(${target} ${tll})
    if(OSX_FRAMEWORK)
        set_target_properties(${target} PROPERTIES INSTALL_RPATH "@executable_path/../../Library/Frameworks")
    endif()
    set(INSTALL_TARGETS ${INSTALL_TARGETS} ${target})
endmacro()

add_exe(qhull src/qhull/unix_r.c ${LIB_NAME_qhull_R})
add_exe(rbox src/rbox/rbox.c ${LIB_NAME_qhull})
add_exe(qconvex src/qconvex/qconvex.c ${LIB_NAME_qhull})
add_exe(qdelaunay src/qdelaunay/qdelaun.c ${LIB_NAME_qhull})
add_exe(qvoronoi src/qvoronoi/qvoronoi.c ${LIB_NAME_qhull})
add_exe(qhalf src/qhalf/qhalf.c ${LIB_NAME_qhull})

# ---------------------------------------
# Define options for linking to qhull_SHAREDR or qhull_SHARED
# ---------------------------------------
if(MSVC)
    set(user_eg_DEFINES qh_dllimport)
    set(user_eg2_DEFINES qh_dllimport)
    set(user_eg3_DEFINES qh_dllimport)
    set(user_egp_DEFINES qh_QHpointer_dllimport qh_QHpointer)
    set(qhullp_DEFINES qh_QHpointer_dllimport qh_QHpointer)
else()
    set(user_eg_DEFINES )
    set(user_eg2_DEFINES )
    set(user_eg3_DEFINES )
    set(user_egp_DEFINES )
    set(qhullp_DEFINES )
endif()

# ---------------------------------------
# Define testqset linked to qset.o and mem.o
# Define testqset_r linked to qset_r.o and mem_r.o
# ---------------------------------------

add_executable(testqset ${testqset_SOURCES})
add_executable(testqset_r ${testqsetr_SOURCES})

add_exe(user_eg src/user_eg/user_eg_r.c ${LIB_NAME_qhull_R})
set_target_properties(user_eg PROPERTIES
    COMPILE_DEFINITIONS "${user_eg_DEFINES}")

# ---------------------------------------
# Define user_eg2 linked to reentrant qhull static library
# ---------------------------------------

add_exe(user_eg2 src/user_eg2/user_eg2_r.c ${LIB_NAME_qhull_R})
add_exe(user_eg3 src/user_eg3/user_eg3_r.cpp "${LIB_NAME_qhull_R};${LIB_NAME_qhull_CPP}")

# ---------------------------------------
# qhullp is qhull/unix.c linked to deprecated qh_QHpointer libqhull_p
# Included for testing qh_QHpointer
# ---------------------------------------

add_exe(qhullp src/qhull/unix.c ${LIB_NAME_qhull_P})
set_target_properties(qhullp PROPERTIES
    COMPILE_DEFINITIONS "${qhullp_DEFINES}")

add_exe(user_egp src/user_eg/user_eg.c ${LIB_NAME_qhull_P})
set_target_properties(user_egp PROPERTIES
    COMPILE_DEFINITIONS "${user_egp_DEFINES}")

# ---------------------------------------
# Define test
# ---------------------------------------

enable_testing()
add_test(NAME testqset
   COMMAND ./testqset 10000)
add_test(NAME testqset_r
   COMMAND ./testqset_r 10000)
add_test(NAME smoketest
   COMMAND sh -c "./rbox D4 | ./qhull Tv")
add_test(NAME rbox-10-qhull
   COMMAND sh -c "./rbox 10 | ./qhull Tv")
add_test(NAME rbox-10-qconvex
   COMMAND sh -c "./rbox 10 | ./qconvex Tv")
add_test(NAME rbox-10-qdelaunay
   COMMAND sh -c "./rbox 10 | ./qdelaunay Tv")
add_test(NAME rbox-10-qhalf
   COMMAND sh -c "./rbox 10 | ./qconvex FQ FV n Tv | ./qhalf Tv")
add_test(NAME rbox-10-qvoronoi
   COMMAND sh -c "./rbox 10 | ./qvoronoi Tv")
add_test(NAME user_eg
   COMMAND sh -c "./user_eg")
add_test(NAME user_eg2
   COMMAND sh -c "./user_eg2")
add_test(NAME user_eg3
   COMMAND sh -c "./user_eg3 rbox '10 D2' '2 D2' qhull 's p' facets")

set(qhull_TARGETS
    # ${LIB_NAME_qhull_CPP}
    ${LIB_NAME_qhull}
    ${LIB_NAME_qhull_P}
    ${LIB_NAME_qhull_R}
)
set(qhull_TARGETS_INSTALL ${qhull_TARGETS}
    qhull rbox qconvex qdelaunay qvoronoi qhalf
)

if (REGISTER_PACKAGE)
    export(TARGETS ${qhull_TARGETS} FILE ${PROJECT_NAME}-exports.cmake)

    set(EXPORT_PACKAGE_NAME QHULL)
    string(TOUPPER ${EXPORT_PACKAGE_NAME} EXPORT_PACKAGE_NAME_UPPER)
    set(EXPORT_PACKAGE_LIB_NAME ${PROJECT_NAME})

    export(PACKAGE ${EXPORT_PACKAGE_NAME})

    include(CMakePackageConfigHelpers)
    configure_package_config_file(
        ${CMAKE_SOURCE_DIR}/cmake/PackageConfig.cmake.in
        ${CMAKE_CURRENT_BINARY_DIR}/${EXPORT_PACKAGE_NAME}Config.cmake
        INSTALL_DESTINATION ${CMAKE_CURRENT_BINARY_DIR} )
    write_basic_package_version_file(
        ${CMAKE_CURRENT_BINARY_DIR}/${EXPORT_PACKAGE_NAME}ConfigVersion.cmake
        VERSION ${VERSION}
        COMPATIBILITY AnyNewerVersion )
else()
    export(TARGETS ${qhull_TARGETS} FILE ${PROJECT_NAME}-exports.cmake EXPORT_LINK_INTERFACE_LIBRARIES)
endif()

if(NOT SKIP_INSTALL_LIBRARIES AND NOT SKIP_INSTALL_ALL)
    install(TARGETS ${qhull_TARGETS_INSTALL}
        RUNTIME DESTINATION ${INSTALL_BIN_DIR} COMPONENT applications
        ARCHIVE DESTINATION ${INSTALL_LIB_DIR} COMPONENT libraries
        LIBRARY DESTINATION ${INSTALL_LIB_DIR} COMPONENT libraries
        FRAMEWORK DESTINATION ${INSTALL_LIB_DIR}
    )
endif()

if (NOT SKIP_INSTALL_DOCS AND NOT SKIP_INSTALL_ALL)
    install(FILES html/qhull.man         DESTINATION ${INSTALL_MAN_DIR} RENAME qhull.1)
    install(FILES html/rbox.man          DESTINATION ${INSTALL_MAN_DIR} RENAME rbox.1)
    install(FILES ${doc_FILES}           DESTINATION ${INSTALL_DOC_DIR})
    install(DIRECTORY html/              DESTINATION ${INSTALL_DOC_DIR})
    install(FILES ${libqhull_DOC}        DESTINATION ${INSTALL_DOC_DIR}/libqhull)
    install(FILES ${libqhullr_DOC}        DESTINATION ${INSTALL_DOC_DIR}/libqhull_r)
endif()

if (NOT SKIP_INSTALL_HEADERS AND NOT SKIP_INSTALL_ALL)
    install(FILES ${libqhull_HEADERS}    DESTINATION ${INSTALL_INC_DIR}/libqhull)
    install(FILES ${libqhullr_HEADERS}    DESTINATION ${INSTALL_INC_DIR}/libqhull_r)
    install(FILES ${libqhullcpp_HEADERS} DESTINATION ${INSTALL_INC_DIR}/libqhullcpp)
endif()
