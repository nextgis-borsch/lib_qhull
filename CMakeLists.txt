################################################################################
# Project:  Lib QHull
# Purpose:  CMake build scripts
# Author:   Dmitry Baryshnikov, dmitry.baryshnikov@nexgis.com
################################################################################
# Copyright (C) 2017-2018, NextGIS <info@nextgis.com>
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
  set(INSTALL_BIN_DIR "bin" CACHE INTERNAL "Installation directory for executables" FORCE)
  set(INSTALL_LIB_DIR "Library/Frameworks" CACHE INTERNAL "Installation directory for libraries" FORCE)
  set(INSTALL_INC_DIR "${INSTALL_LIB_DIR}/${PROJECT_NAME}.framework/Headers" CACHE INTERNAL "Installation directory for headers" FORCE)
  set(INSTALL_CMAKECONF_DIR ${INSTALL_LIB_DIR}/${PROJECT_NAME}.framework/Resources/CMake CACHE INTERNAL "Installation directory for cmake config files" FORCE)
  set(SKIP_INSTALL_HEADERS ON)
  set(SKIP_INSTALL_FILES ON)
  set(SKIP_INSTALL_EXPORT ON)
  set(CMAKE_MACOSX_RPATH ON)
  set(SKIP_INSTALL_DOCS ON)
else()
    include(GNUInstallDirs)

    set(INSTALL_BIN_DIR ${CMAKE_INSTALL_BINDIR} CACHE INTERNAL "Installation directory for executables" FORCE)
    set(INSTALL_LIB_DIR ${CMAKE_INSTALL_LIBDIR} CACHE INTERNAL "Installation directory for libraries" FORCE)
    set(INSTALL_INC_DIR ${CMAKE_INSTALL_INCLUDEDIR} CACHE INTERNAL "Installation directory for headers" FORCE)
    set(INSTALL_DOC_DIR ${CMAKE_INSTALL_DOCDIR} CACHE INTERNAL "Share directory for documents" FORCE)
    set(INSTALL_MAN_DIR ${CMAKE_INSTALL_MANDIR} CACHE INTERNAL "Share directory for manuals" FORCE)
    set(INSTALL_CMAKECONF_DIR ${CMAKE_INSTALL_DATADIR}/${PROJECT_NAME}/CMake CACHE INTERNAL "Installation directory for cmake config files" FORCE)
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

set(doc_FILES
    README.txt
    REGISTER.txt
    Announce.txt
    COPYING.txt
    index.htm
)

include_directories(${CMAKE_SOURCE_DIR}/src)

set(LIB_NAME_qhull_CPP qhullcpp)
set(LIB_NAME_qhull qhull)  # Temporarily avoid name conflict with qhull executable
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
            IMPORT_SUFFIX "_i.lib"
        )
    endif()
elseif(OSX_FRAMEWORK)
    add_library(${LIB_NAME_qhull} SHARED  ${libqhull_SOURCES} ${libqhull_HEADERS}
    src/libqhull/qhull-exports.def)
    set_property(SOURCE ${libqhull_HEADERS}
      PROPERTY MACOSX_PACKAGE_LOCATION Headers/libqhull
    )
    set_target_properties(${LIB_NAME_qhull} PROPERTIES
      FRAMEWORK TRUE
      FRAMEWORK_VERSION ${FRAMEWORK_VERSION}
      MACOSX_FRAMEWORK_SHORT_VERSION_STRING ${VERSION}
      MACOSX_FRAMEWORK_BUNDLE_VERSION ${VERSION}
      MACOSX_FRAMEWORK_IDENTIFIER org.libqhull.libqhull
      XCODE_ATTRIBUTE_INSTALL_PATH "@rpath"
      # PUBLIC_HEADER "${libqhull_HEADERS}"
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
    set_property(SOURCE ${libqhullr_HEADERS}
      PROPERTY MACOSX_PACKAGE_LOCATION Headers/libqhull_r
    )
    set_target_properties(${LIB_NAME_qhull_R} PROPERTIES
      FRAMEWORK TRUE
      FRAMEWORK_VERSION ${FRAMEWORK_VERSION}
      MACOSX_FRAMEWORK_SHORT_VERSION_STRING ${VERSION}
      MACOSX_FRAMEWORK_BUNDLE_VERSION ${VERSION}
      MACOSX_FRAMEWORK_IDENTIFIER org.libqhull.libqhullr
      XCODE_ATTRIBUTE_INSTALL_PATH "@rpath"
      # PUBLIC_HEADER "${libqhullr_HEADERS}"
      VERSION ${VERSION}
      SOVERSION ${SOVERSION}
      )
else()
    add_library(${LIB_NAME_qhull_R} STATIC  ${libqhullr_SOURCES} ${libqhullr_HEADERS})
endif()

if(UNIX)
    target_link_libraries(${LIB_NAME_qhull_R} m)
endif()

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

if(BUILD_SHARED_LIBS)
    add_library(${LIB_NAME_qhull_P} SHARED ${libqhull_SOURCES} ${libqhull_HEADERS}
    src/libqhull/qhull_p-exports.def)
    set_target_properties (${LIB_NAME_qhull_P} PROPERTIES
        VERSION ${VERSION}
        SOVERSION ${SOVERSION}
    )
    if(WIN32)
        set_target_properties(${LIB_NAME_qhull_P} PROPERTIES IMPORT_SUFFIX "_i.lib" COMPILE_DEFINITIONS "${qhullp_DEFINES}")
    endif()
elseif(OSX_FRAMEWORK)
    add_library(${LIB_NAME_qhull_P} SHARED  ${libqhull_SOURCES} ${libqhull_HEADERS}
    src/libqhull/qhull_p-exports.def)
    set_property(SOURCE ${libqhull_HEADERS}
      PROPERTY MACOSX_PACKAGE_LOCATION Headers/libqhull
    )
    set_target_properties(${LIB_NAME_qhull_P} PROPERTIES
      FRAMEWORK TRUE
      FRAMEWORK_VERSION ${FRAMEWORK_VERSION}
      MACOSX_FRAMEWORK_SHORT_VERSION_STRING ${VERSION}
      MACOSX_FRAMEWORK_BUNDLE_VERSION ${VERSION}
      MACOSX_FRAMEWORK_IDENTIFIER org.libqhull.libqhullp
      XCODE_ATTRIBUTE_INSTALL_PATH "@rpath"
      # PUBLIC_HEADER "${libqhull_HEADERS}"
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

add_exe(qhull-app src/qhull/unix_r.c ${LIB_NAME_qhull_R})
set_target_properties (qhull-app PROPERTIES
    OUTPUT_NAME "qhull"
)
add_exe(rbox src/rbox/rbox.c ${LIB_NAME_qhull})
add_exe(qconvex src/qconvex/qconvex.c ${LIB_NAME_qhull})
add_exe(qdelaunay src/qdelaunay/qdelaun.c ${LIB_NAME_qhull})
add_exe(qvoronoi src/qvoronoi/qvoronoi.c ${LIB_NAME_qhull})
add_exe(qhalf src/qhalf/qhalf.c ${LIB_NAME_qhull})

# ---------------------------------------
# Define testqset linked to qset.o and mem.o
# Define testqset_r linked to qset_r.o and mem_r.o
# ---------------------------------------

add_executable(testqset ${testqset_SOURCES})
add_executable(testqset_r ${testqsetr_SOURCES})

# add_exe(user_eg src/user_eg/user_eg_r.c ${LIB_NAME_qhull_R})
# set_target_properties(user_eg PROPERTIES
#     COMPILE_DEFINITIONS "${user_eg_DEFINES}")

# ---------------------------------------
# Define user_eg2 linked to reentrant qhull static library
# ---------------------------------------

# add_exe(user_eg2 src/user_eg2/user_eg2_r.c ${LIB_NAME_qhull_R})
# add_exe(user_eg3 "src/user_eg3/user_eg3_r.cpp;${libqhullcpp_SOURCES}" ${LIB_NAME_qhull_R})

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
# add_test(user_eg_1 user_eg "QR1 p n Qt" "v p" Fp)
# add_test(user_eg2_1 user_eg2 "QR1 p" "v p" Fp)
# add_test(user_eg3_1 user_eg3 rbox "10 D2" "2 D2" qhull "p")

add_test(qconvex_1 qconvex -)
add_test(qconvex_2 qconvex .)
# add_test(qconvex_3 qconvex)
if(UNIX)
    add_test(NAME rbox_qconvex_1 COMMAND sh -c "./rbox c D3 | ./qconvex s n Qt")
    add_test(NAME rbox_qconvex_2 COMMAND sh -c "./rbox c D2 | ./qconvex i Qt")
    add_test(NAME rbox_qconvex_3 COMMAND sh -c "./rbox c D2 | ./qconvex o")
    add_test(NAME rbox_qconvex_4 COMMAND sh -c "./rbox 1000 s | ./qconvex s Tv FA")
    add_test(NAME rbox_qconvex_5 COMMAND sh -c "./rbox c d D2 | ./qconvex s Qc Fx")
    add_test(NAME rbox_qconvex_6 COMMAND sh -c "./rbox y 1000 W0 | ./qconvex s n")
    add_test(NAME rbox_qconvex_7 COMMAND sh -c "./rbox y 1000 W0 | ./qconvex s QJ")
    add_test(NAME rbox_qconvex_8 COMMAND sh -c "./rbox d G1 D12 | ./qconvex QR0 FA")
    add_test(NAME rbox_qconvex_9 COMMAND sh -c "./rbox c D6 | ./qconvex FA TF500")
    add_test(NAME rbox_qconvex_10 COMMAND sh -c "./rbox c P0 d D2 | ./qconvex p Fa Fc FP FI Fn FN FS Fv Fx")
    add_test(NAME rbox_qconvex_11 COMMAND sh -c "./rbox c d D2 | ./qconvex s i QV0")
    # add_test(NAME rbox_qconvex_12 COMMAND sh -c "./rbox c | ./qconvex Q0")
endif()
add_test(qvoronoi_1 qvoronoi -)
add_test(qvoronoi_2 qvoronoi .)
# add_test(qvoronoi_3 qvoronoi)
if(UNIX)
    add_test(NAME rbox_qvoronoi_1 COMMAND sh -c "./rbox c P0 D2 | ./qvoronoi s o")
    add_test(NAME rbox_qvoronoi_2 COMMAND sh -c "./rbox c P0 D2 | ./qvoronoi Fi")
    add_test(NAME rbox_qvoronoi_3 COMMAND sh -c "./rbox c P0 D2 | ./qvoronoi Fo")
    add_test(NAME rbox_qvoronoi_4 COMMAND sh -c "./rbox c P0 D2 | ./qvoronoi Fv")
    add_test(NAME rbox_qvoronoi_5 COMMAND sh -c "./rbox c P0 D2 | ./qvoronoi s Qu Qt Fv")
    add_test(NAME rbox_qvoronoi_6 COMMAND sh -c "./rbox c P0 D2 | ./qvoronoi Qu Fo")
    add_test(NAME rbox_qvoronoi_7 COMMAND sh -c "./rbox c G1 d D2 | ./qvoronoi s p ")
    add_test(NAME rbox_qvoronoi_8 COMMAND sh -c "./rbox c G1 d D2 | ./qvoronoi QJ p ")
    add_test(NAME rbox_qvoronoi_9 COMMAND sh -c "./rbox c P-0.1 P+0.1 P+0.1 D2 | ./qvoronoi s Fc FP FQ Fn FN ")
    add_test(NAME rbox_qvoronoi_10 COMMAND sh -c "./rbox P0 c D2 | ./qvoronoi s Fv QV0")
endif()
add_test(qdelaunay_1 qdelaunay -)
add_test(qdelaunay_2 qdelaunay .)
# add_test(qdelaunay_3 qdelaunay)
if(UNIX)
    add_test(NAME rbox_delaunay_1 COMMAND sh -c "./rbox c P0 D2 | ./qdelaunay s o")
    add_test(NAME rbox_delaunay_2 COMMAND sh -c "./rbox c P0 D2 | ./qdelaunay i")
    add_test(NAME rbox_delaunay_3 COMMAND sh -c "./rbox c P0 D2 | ./qdelaunay Fv")
    add_test(NAME rbox_delaunay_4 COMMAND sh -c "./rbox c P0 D2 | ./qdelaunay s Qu Qt Fv")
    add_test(NAME rbox_delaunay_5 COMMAND sh -c "./rbox c G1 d D2 | ./qdelaunay s i")
    # add_test(NAME rbox_delaunay_6 COMMAND sh -c "./rbox c G1 d D2 | ./qdelaunay Ft")
    # add_test(NAME rbox_delaunay_7 COMMAND sh -c "./rbox c G1 d D2 | ./qdelaunay QJ s Ft")
    add_test(NAME rbox_delaunay_8 COMMAND sh -c "./rbox M3,4 z 100 D2 | ./qdelaunay s")
    add_test(NAME rbox_delaunay_9 COMMAND sh -c "./rbox c P-0.1 P+0.1 P+0.1 D2 | ./qdelaunay s Fx Fa Fc FP FQ Fn FN")
    add_test(NAME rbox_delaunay_10 COMMAND sh -c "./rbox P0 P0 c D2 | ./qdelaunay s FP QV0")
endif()
add_test(qhalf_1 qhalf -)
add_test(qhalf_2 qhalf .)
# add_test(qhalf_3 qhalf)
if(UNIX)
    add_test(NAME rbox_qhull_qhalf_1 COMMAND sh -c "./rbox d | ./qhull FQ n | ./qhalf s H0,0,0 Fp")
    add_test(NAME rbox_qhull_qhalf_2 COMMAND sh -c "./rbox c | ./qhull FQ FV n | ./qhalf o")
    add_test(NAME rbox_qhull_qhalf_3 COMMAND sh -c "./rbox d D2 | ./qhull FQ n | ./qhalf s H0 Fc FP Fn FN FQ Fv Fx")
    # add_test(NAME rbox_qhull_1 COMMAND sh -c "./rbox 1000 W0 t | ./qhull QR2 QJ s Fs Tv")
    # add_test(NAME rbox_qhull_2 COMMAND sh -c "./rbox 1000 W0 t | ./qhull QR2 s Fs Tv")
    # add_test(NAME rbox_qhull_3 COMMAND sh -c "./rbox 1000 s t | ./qhull C0.02 Qc Tv")
    # add_test(NAME rbox_qhull_4 COMMAND sh -c "./rbox 500 s D4 t | ./qhull C0.01 Qc Tv")
    # add_test(NAME rbox_qhull_5 COMMAND sh -c "./rbox 1000 s t | ./qhull C-0.02 Qc Tv")
    # add_test(NAME rbox_qhull_6 COMMAND sh -c "./rbox 1000 s D4 t | ./qhull C-0.01 Qc Tv")
    # add_test(NAME rbox_qhull_7 COMMAND sh -c "./rbox 200 s D5 t | ./qhull C-0.01 Qx Qc Tv")
    # add_test(NAME rbox_qhull_8 COMMAND sh -c "./rbox 100 s D6 t | ./qhull C-0.001 Qx Qc Tv")
    # add_test(NAME rbox_qhull_9 COMMAND sh -c "./rbox 1000 W1e-4 t | ./qhull C-1e-6 Qc Tv")
    # add_test(NAME rbox_qhull_10 COMMAND sh -c "./rbox 1000 W5e-4 D4 t | ./qhull C-1e-5 Qc Tv")
    # add_test(NAME rbox_qhull_11 COMMAND sh -c "./rbox 400 W1e-3 D5 t | ./qhull C-1e-5 Qx Qc Tv")
    add_test(NAME rbox_qhull_12 COMMAND sh -c "./rbox d h | ./qhull Fd FV n FD  Tcv | ./qhull Fd H Fp Tcv")
    add_test(NAME rbox_qhull_13 COMMAND sh -c "./rbox 10 h | ./qhull Fd FD p Tcv | ./qhull Fd d Tcv ")
endif()
add_test(rbox_1 rbox 3 n D2)
add_test(rbox_2 rbox 3 n D2)
add_test(rbox_3 rbox 3 D2)
add_test(rbox_4 rbox 3 h D2)
add_test(rbox_5 rbox 3 z D2)
add_test(rbox_6 rbox 3 z h D2)
add_test(rbox_7 rbox 3 B10 D2)
add_test(rbox_8 rbox 3 z B10 D2)
add_test(rbox_9 rbox 4 L2 r D2)
add_test(rbox_10 rbox 8 L2 D2)
add_test(rbox_11 rbox 4 L4 r D3)
add_test(rbox_12 rbox y)
add_test(rbox_13 rbox 10 M3,4)
add_test(rbox_14 rbox 4 L4 s D5 W1e-3)

if(UNIX)
    add_test(NAME rbox_qhull_14 COMMAND sh -c "./rbox 10 L2 s D3 | ./qhull Tcv")
    add_test(NAME rbox_qhull_15 COMMAND sh -c "./rbox 10 L4 s W1e-3 D3 | ./qhull Tcv")
    add_test(NAME rbox_qhull_16 COMMAND sh -c "./rbox 10 L6 D3 | ./qhull Tcv")
    add_test(NAME rbox_qhull_17 COMMAND sh -c "./rbox 10 L1.1 s D4 | ./qhull Tcv")
    add_test(NAME rbox_qhull_18 COMMAND sh -c "./rbox y r 100 W0 O0.5 | ./qhull s p Tcv")
    add_test(NAME rbox_qhull_19 COMMAND sh -c "./rbox x r 100 W0 O0.5 | ./qhull s p Tcv")
    add_test(NAME rbox_qhull_20 COMMAND sh -c "./rbox 12 D8 | ./qhull Tcv")
    add_test(NAME rbox_qhull_21 COMMAND sh -c "./rbox 12 D9 | ./qhull Tcv")
    add_test(NAME rbox_qhull_22 COMMAND sh -c "./rbox 1000 D4 | ./qhull s i A-0.97 C0.2 A0.7 Tcv")
    add_test(NAME rbox_qhull_23 COMMAND sh -c "./rbox 3 D2 | ./qhull Qb0B1:-2 p")
    add_test(NAME rbox_qhull_24 COMMAND sh -c "./rbox 100 r D2 | ./qhull Pd0:0.7 PD0:0.8 n Tcv")
    add_test(NAME rbox_qhull_25 COMMAND sh -c "./rbox 1000 s | ./qhull  C0.05 Tcv")
    # add_test(NAME rbox_qhull_26 COMMAND sh -c "./rbox 1000 s t | ./qhull Qm C0.05 Tcv")
    add_test(NAME rbox_qhull_27 COMMAND sh -c "./rbox 500 D2 | ./qhull n A-0.95 C0.1 Tcv")
    add_test(NAME rbox_qhull_28 COMMAND sh -c "./rbox 500 s P1,1,1 | ./qhull QgG0 Pp Tcv")
    add_test(NAME rbox_qhull_29 COMMAND sh -c "./rbox d | ./qhull m")
    add_test(NAME rbox_qhull_30 COMMAND sh -c "./rbox d | ./qhull FM")
    add_test(NAME rbox_qhull_31 COMMAND sh -c "./rbox c D2 | ./qhull Q0 Tcv")
    add_test(NAME rbox_qhull_32 COMMAND sh -c "./rbox d D2 | ./qhull Tcv")
    add_test(NAME rbox_qhull_33 COMMAND sh -c "./rbox c D3 | ./qhull Q0 Tcv")
    add_test(NAME rbox_qhull_34 COMMAND sh -c "./rbox d D3 | ./qhull Tcv")
    add_test(NAME rbox_qhull_35 COMMAND sh -c "./rbox c D4 | ./qhull Q0 Tcv")
    add_test(NAME rbox_qhull_36 COMMAND sh -c "./rbox d D4 | ./qhull Tcv")
    add_test(NAME rbox_qhull_37 COMMAND sh -c "./rbox c D5 | ./qhull Q0 Tcv")
    add_test(NAME rbox_qhull_38 COMMAND sh -c "./rbox d D5 | ./qhull Tcv")
    add_test(NAME rbox_qhull_39 COMMAND sh -c "./rbox c D6 | ./qhull Q0 Tcv")
    add_test(NAME rbox_qhull_40 COMMAND sh -c "./rbox d D6 | ./qhull Tcv")
    add_test(NAME rbox_qhull_41 COMMAND sh -c "./rbox d D7 | ./qhull Tcv")
    add_test(NAME rbox_qhull_42 COMMAND sh -c "./rbox c D2 | ./qhull Tcv C-0")
    add_test(NAME rbox_qhull_43 COMMAND sh -c "./rbox c D3 | ./qhull Tcv C-0")
    add_test(NAME rbox_qhull_44 COMMAND sh -c "./rbox c D4 | ./qhull Tcv C-0")
    add_test(NAME rbox_qhull_45 COMMAND sh -c "./rbox c D5 | ./qhull Tcv C-0")
    add_test(NAME rbox_qhull_46 COMMAND sh -c "./rbox c D6 | ./qhull Tcv C-0")
    add_test(NAME rbox_qhull_47 COMMAND sh -c "./rbox c D7 | ./qhull Tv C-0")
    add_test(NAME rbox_qhull_48 COMMAND sh -c "./rbox 20 l D3 | ./qhull Tcv")
    add_test(NAME rbox_qhull_49 COMMAND sh -c "./rbox 100 s D2 | ./qhull Tcv")
    add_test(NAME rbox_qhull_50 COMMAND sh -c "./rbox 100 s D3 | ./qhull Tcv")
    add_test(NAME rbox_qhull_51 COMMAND sh -c "./rbox 100 s D4 | ./qhull Tcv")
    add_test(NAME rbox_qhull_52 COMMAND sh -c "./rbox 100 s c D4 | ./qhull Tcv")
    add_test(NAME rbox_qhull_53 COMMAND sh -c "./rbox 100 s d G1.5 D4 | ./qhull Tcv")
    add_test(NAME rbox_qhull_54 COMMAND sh -c "./rbox 100 s W1e-2 | ./qhull Tcv")
    add_test(NAME rbox_qhull_55 COMMAND sh -c "./rbox 100 | ./qhull Tcv")
    add_test(NAME rbox_qhull_56 COMMAND sh -c "./rbox 100 W1e-3 | ./qhull Tcv")
    add_test(NAME rbox_qhull_57 COMMAND sh -c "./rbox 100 r D2 | ./qhull Tcv")
    add_test(NAME rbox_qhull_58 COMMAND sh -c "./rbox 100 r s Z1 | ./qhull Tcv")
    add_test(NAME rbox_qhull_59 COMMAND sh -c "./rbox 100 r s Z1 G0.1 | ./qhull Tcv C-0")
    add_test(NAME rbox_qhull_60 COMMAND sh -c "./rbox 100 s Z1 G0.1 | ./qhull Tcv")
    add_test(NAME rbox_qhull_61 COMMAND sh -c "./rbox 100 s Z1e-5 G0.1 | ./qhull Tc Pp")
    add_test(NAME rbox_qhull_62 COMMAND sh -c "./rbox 5 r s D2 | ./qhull Tcv")
    add_test(NAME rbox_qhull_63 COMMAND sh -c "./rbox 5 r s D2 | ./qhull s")
    add_test(NAME rbox_qhull_64 COMMAND sh -c "./rbox 5 r s D2 | ./qhull s o")
    add_test(NAME rbox_qhull_65 COMMAND sh -c "./rbox 5 r s D2 | ./qhull f")
    add_test(NAME rbox_qhull_66 COMMAND sh -c "./rbox 5 r s D2 | ./qhull i")
    add_test(NAME rbox_qhull_67 COMMAND sh -c "./rbox 5 r s D2 | ./qhull m")
    add_test(NAME rbox_qhull_68 COMMAND sh -c "./rbox 5 r s D2 | ./qhull FM")
    add_test(NAME rbox_qhull_69 COMMAND sh -c "./rbox 5 r s D2 | ./qhull n")
    add_test(NAME rbox_qhull_70 COMMAND sh -c "./rbox 5 r s D2 | ./qhull p")
    add_test(NAME rbox_qhull_71 COMMAND sh -c "./rbox 5 r s D2 | ./qhull o")
    add_test(NAME rbox_qhull_72 COMMAND sh -c "./rbox 5 r s D2 | ./qhull Fx")
    add_test(NAME rbox_qhull_73 COMMAND sh -c "./rbox 5 r s D2 | ./qhull p n i p p")
    add_test(NAME rbox_qhull_74 COMMAND sh -c "./rbox 10 D3 | ./qhull f Tcv")
    add_test(NAME rbox_qhull_75 COMMAND sh -c "./rbox 10 D3 | ./qhull i")
    add_test(NAME rbox_qhull_76 COMMAND sh -c "./rbox 10 D3 | ./qhull p")
    add_test(NAME rbox_qhull_77 COMMAND sh -c "./rbox 10 D3 | ./qhull o")
    add_test(NAME rbox_qhull_78 COMMAND sh -c "./rbox 10 D3 | ./qhull Fx")
    add_test(NAME rbox_qhull_79 COMMAND sh -c "./rbox 27 M1,0,1 | ./qhull Qc")
    add_test(NAME rbox_qhull_80 COMMAND sh -c "./rbox 50 D3 s | ./qhull C0.1 Qc Pd0d1d2 s p Tcv")
    add_test(NAME rbox_qhull_81 COMMAND sh -c "./rbox 10 D2 P0 P1e-15 | ./qhull d Qc FP s Tcv")
    add_test(NAME rbox_qhull_82 COMMAND sh -c "./rbox 100 s | ./qhull C-0.003 Qc FP s")
    add_test(NAME rbox_qhull_83 COMMAND sh -c "./rbox 100 s D2 | ./qhull C0.1 i Fx Tcv")
    add_test(NAME rbox_qhull_84 COMMAND sh -c "./rbox 4 s D3 | ./qhull Qc Ghipv Tcv")
    add_test(NAME rbox_qhull_85 COMMAND sh -c "./rbox 6 D4 | ./qhull f Tcv")
    add_test(NAME rbox_qhull_86 COMMAND sh -c "./rbox 6 D4 | ./qhull i")
    add_test(NAME rbox_qhull_87 COMMAND sh -c "./rbox 6 D4 | ./qhull p")
    add_test(NAME rbox_qhull_88 COMMAND sh -c "./rbox 6 D4 | ./qhull o")
    add_test(NAME rbox_qhull_89 COMMAND sh -c "./rbox 1000 s D2 | ./qhull FA Tcv")
    add_test(NAME rbox_qhull_90 COMMAND sh -c "./rbox 1000 s | ./qhull FA Tcv")
    add_test(NAME rbox_qhull_91 COMMAND sh -c "./rbox c D4 | ./qhull FA Tcv")
    add_test(NAME rbox_qhull_92 COMMAND sh -c "./rbox c D5 | ./qhull FA Tcv")
    add_test(NAME rbox_qhull_93 COMMAND sh -c "./rbox 10 D2 | ./qhull d FA Tcv")
    add_test(NAME rbox_qhull_94 COMMAND sh -c "./rbox 10 D2 | ./qhull d Qu FA Tcv")
    add_test(NAME rbox_qhull_95 COMMAND sh -c "./rbox 10 D2 | ./qhull FA Tcv")
    add_test(NAME rbox_qhull_96 COMMAND sh -c "./rbox 10 c D2 | ./qhull Fx Tcv")
    add_test(NAME rbox_qhull_97 COMMAND sh -c "./rbox 1000 s | ./qhull FS Tcv")
    add_test(NAME rbox_qhull_98 COMMAND sh -c "./rbox 10 W0 D2 | ./qhull p Qc FcC Tcv")
    add_test(NAME rbox_qhull_99 COMMAND sh -c "./rbox 4 z h s D2 | ./qhull Fd s n FD Tcv")
    add_test(NAME rbox_qhull_100 COMMAND sh -c "./rbox 6 s D3 | ./qhull C-0.1 Qc FF s FQ Fi n Fo FQ FI Fm Fn FN FO FO FQ Fs FS FV Fv Tcv")
    add_test(NAME rbox_qhull_101 COMMAND sh -c "./rbox P0.5,0.5 P0.5,0.5 W0 5 D2 | ./qhull d FN Qc")
    add_test(NAME rbox_qhull_102 COMMAND sh -c "./rbox 10 D3 | ./qhull Fa PA5")
    add_test(NAME rbox_qhull_103 COMMAND sh -c "./rbox 10 D3 | ./qhull Fa PF0.4")
    add_test(NAME rbox_qhull_104 COMMAND sh -c "./rbox c | ./qhull Qt s o Tcv")
    add_test(NAME rbox_qhull_105 COMMAND sh -c "./rbox c | ./qhull Qt f i")
    add_test(NAME rbox_qhull_106 COMMAND sh -c "./rbox c | ./qhull Qt m FM n")
    add_test(NAME rbox_qhull_107 COMMAND sh -c "./rbox c | ./qhull Qt p o")
    add_test(NAME rbox_qhull_108 COMMAND sh -c "./rbox c | ./qhull Qt Fx")
    add_test(NAME rbox_qhull_109 COMMAND sh -c "./rbox c | ./qhull Qt FA s Fa")
    add_test(NAME rbox_qhull_110 COMMAND sh -c "./rbox 6 r s c G0.1 D2 | ./qhull Qt d FA Tcv")
    add_test(NAME rbox_qhull_111 COMMAND sh -c "./rbox 6 r s c G0.1 D2 | ./qhull d FA Tcv")
    add_test(NAME rbox_qhull_112 COMMAND sh -c "./rbox 6 r s c G0.1 D2 | ./qhull Qt v p Tcv")
    add_test(NAME rbox_qhull_113 COMMAND sh -c "./rbox c | ./qhull Qt C-0.1 Qc FF s FQ Fi n Fo FQ FI Fm Fn FN FO FO FQ Fs FS FV Fv Tcv")
    add_test(NAME rbox_qhull_114 COMMAND sh -c "./rbox 6 r s c G0.1 D2 P0.1,0.1 | ./qhull s FP d FO Qt")
    # add_test(NAME rbox_qhull_115 COMMAND sh -c "./rbox c | qhull PD0:0.5 n | ./qhull H0 Fp Tcv")
    add_test(NAME rbox_qhull_116 COMMAND sh -c "./rbox 1000 W1e-3 D3 | ./qhull PA8 Fa FS s n Tcv")
    add_test(NAME rbox_qhull_117 COMMAND sh -c "./rbox 1000 W1e-3 D3 | ./qhull C-0.01 PM10 Fm n Tcv Qc")
    add_test(NAME rbox_qhull_118 COMMAND sh -c "./rbox 1000 W1e-3 D3 | ./qhull C-0.01 PA8 PG n Tcv Qc")
    add_test(NAME rbox_qhull_119 COMMAND sh -c "./rbox 10 | ./qhull FO Tz TO q_test.log.1")
    add_test(NAME rbox_qhull_120 COMMAND sh -c "./rbox 10 D2 | ./qhull d Tcv")
    add_test(NAME rbox_qhull_121 COMMAND sh -c "./rbox 10 D2 | ./qhull d Qz Tcv")
    add_test(NAME rbox_qhull_122 COMMAND sh -c "./rbox 10 D3 | ./qhull d Tcv")
    add_test(NAME rbox_qhull_123 COMMAND sh -c "./rbox c | ./qhull d Qz Ft Tcv")
    add_test(NAME rbox_qhull_124 COMMAND sh -c "./rbox 10 s D2 c | ./qhull d Tcv")
    add_test(NAME rbox_qhull_125 COMMAND sh -c "./rbox 10 s D2 | ./qhull d Tcv Qz Q8")
    add_test(NAME rbox_qhull_126 COMMAND sh -c "./rbox 10 D2 | ./qhull d Tcv p")
    add_test(NAME rbox_qhull_127 COMMAND sh -c "./rbox 10 c D2 | ./qhull Fx Tcv")
    # TODO: Add tests
endif()

add_test(NAME testqset COMMAND testqset 10000)
add_test(NAME testqset_r COMMAND testqset_r 10000)

if(UNIX)
    add_test(NAME smoketest COMMAND sh -c "./rbox D4 | ./qhull Tv")
    add_test(NAME rbox-10-qhull COMMAND sh -c "./rbox 10 | ./qhull Tv")
    add_test(NAME rbox-10-qconvex COMMAND sh -c "./rbox 10 | ./qconvex Tv")
    add_test(NAME rbox-10-qdelaunay COMMAND sh -c "./rbox 10 | ./qdelaunay Tv")
    add_test(NAME rbox-10-qhalf COMMAND sh -c "./rbox 10 | ./qconvex FQ FV n Tv | ./qhalf Tv")
    add_test(NAME rbox-10-qvoronoi COMMAND sh -c "./rbox 10 | ./qvoronoi Tv")
endif()

# add_test(NAME user_eg COMMAND user_eg)
# add_test(NAME user_eg2 COMMAND user_eg2)
# add_test(NAME user_eg3 COMMAND user_eg3 rbox "10 D2" "2 D2" qhull "s p" facets)

set(qhull_TARGETS
    ${LIB_NAME_qhull}
)
set(qhull_TARGETS_INSTALL ${qhull_TARGETS}
    ${LIB_NAME_qhull_P}
    ${LIB_NAME_qhull_R}
    qhull-app rbox qconvex qdelaunay qvoronoi qhalf
)

set(PACKAGE_NAME ${PROJECT_NAME})
string(TOUPPER ${PACKAGE_NAME} PACKAGE_UPPER_NAME)

if(NOT SKIP_INSTALL_LIBRARIES AND NOT SKIP_INSTALL_ALL)
    install(TARGETS ${qhull_TARGETS_INSTALL}
        EXPORT ${PACKAGE_UPPER_NAME}Targets
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

# Export package ===============================================================

# Add path to includes to build-tree export
target_include_directories(${qhull_TARGETS} PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)

# Add all targets to the build-tree export set
export(TARGETS ${qhull_TARGETS}
    FILE ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Targets.cmake)

if(REGISTER_PACKAGE)
    # Export the package for use from the build-tree
    # (this registers the build-tree with a global CMake-registry)
    export(PACKAGE ${PACKAGE_UPPER_NAME})
endif()

# Create the <Package>Config.cmake file
configure_file(cmake/PackageConfig.cmake.in
    ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Config.cmake @ONLY)

if(NOT SKIP_INSTALL_LIBRARIES AND NOT SKIP_INSTALL_ALL)
    # Install the <Package>Config.cmake
    install(FILES
      ${PROJECT_BINARY_DIR}/${PACKAGE_UPPER_NAME}Config.cmake
      DESTINATION ${INSTALL_CMAKECONF_DIR} COMPONENT dev)

    # Install the export set for use with the install-tree
    install(EXPORT ${PACKAGE_UPPER_NAME}Targets DESTINATION ${INSTALL_CMAKECONF_DIR} COMPONENT dev)
endif()

# Archiving ====================================================================

set(CPACK_PACKAGE_NAME "${PACKAGE_NAME}")
set(CPACK_PACKAGE_VENDOR "${PACKAGE_VENDOR}")
set(CPACK_PACKAGE_VERSION "${VERSION}")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "${PACKAGE_NAME} Installation")
set(CPACK_PACKAGE_RELOCATABLE TRUE)
set(CPACK_ARCHIVE_COMPONENT_INSTALL ON)
set(CPACK_GENERATOR "ZIP")
set(CPACK_MONOLITHIC_INSTALL ON)
set(CPACK_STRIP_FILES TRUE)

# Get cpack zip archive name
get_cpack_filename(${VERSION} PROJECT_CPACK_FILENAME)
set(CPACK_PACKAGE_FILE_NAME ${PROJECT_CPACK_FILENAME})

include(CPack)
