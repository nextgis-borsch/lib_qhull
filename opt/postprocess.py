#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
##
## Project: NextGIS Borsch build system
## Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
##
## Copyright (c) 2017 NextGIS <info@nextgis.com>
## License: GPL v.2
##
## Purpose: Post processing script
################################################################################

import fileinput
import os
import sys
import shutil

cmake_src_path = os.path.join(sys.argv[1], 'CMakeLists.txt')

if not os.path.exists(cmake_src_path):
    exit('Parse path not exists')

utilfile = os.path.join(os.getcwd(), os.pardir, 'cmake', 'util.cmake')

# Get values
version_str = "0"
version2_str = "0"
soversion_str = "0"

version_str_get = False
version2_str_get = False
soversion_str_get = False

def extract_value(text):
    val_text = text.split("\"")
    return val_text[1]

def extract_value2(text):
    val_text = text.split()
    val_text = val_text[1].split(')')
    return val_text[0]

with open(cmake_src_path) as f:
    for line in f:
        if "set(qhull_VERSION2" in line:
            version2_str = extract_value(line)
            version2_str_get = True
        elif "set(qhull_VERSION" in line:
            version_str = extract_value(line)
            version_str_get = True
        elif "set(qhull_SOVERSION" in line:
            soversion_str = extract_value2(line)
            soversion_str_get = True

        if version_str_get and version2_str_get and soversion_str_get:
            break

print version_str
print version2_str
print soversion_str

for line in fileinput.input(utilfile, inplace = 1):
    if "set(VERSION " in line:
        print "    set(VERSION " + version_str + ")"
    elif "set(VERSION2 " in line:
            print "    set(VERSION2 " + version2_str + ")"
    elif "set(SOVERSION " in line:
            print "    set(SOVERSION " + soversion_str + ")"
    else:
        print line,
