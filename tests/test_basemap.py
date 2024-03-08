#!/usr/bin/python3

# Copyright (c) 2022, 2023 Humanitarian OpenStreetMap Team
#
# This file is part of osm_fieldwork.
#
#     Underpass is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Underpass is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with osm_fieldwork.  If not, see <https:#www.gnu.org/licenses/>.
#
"""Test functionalty of basemapper.py."""

import io
import logging
import os
import shutil

from osm_fieldwork.basemapper import BaseMapper
from osm_fieldwork.sqlite import DataFile

log = logging.getLogger(__name__)

rootdir = os.path.dirname(os.path.abspath(__file__))
boundary = f"{rootdir}/testdata/Rollinsville.geojson"
outfile = f"{rootdir}/testdata/rollinsville.mbtiles"
boundary_geojson = f"{rootdir}/testdata/Rollinsville.geojson"
boundary_bbox = "-105.642662 39.917580 -105.631343 39.929250"  # Example BBOX string
base = "./tiles"
# boundary = open(infile, "r")
# poly = geojson.load(boundary)
# if "features" in poly:
#    geometry = shape(poly["features"][0]["geometry"])
# elif "geometry" in poly:
#    geometry = shape(poly["geometry"])
# else:
#    geometry = shape(poly)


def test_create_with_geojson():
    """Test loading with a GeoJSON boundary."""
    hits = 0
    basemap = BaseMapper(boundary, base, "topo", False)
    tiles = list()
    for level in [8, 9, 10, 11, 12]:
        basemap.getTiles(level)
        tiles += basemap.tiles

    if len(tiles) == 5:
        hits += 1

    if tiles[0].x == 52 and tiles[1].y == 193 and tiles[2].x == 211:
        hits += 1

    outf = DataFile(outfile, basemap.getFormat())
    outf.writeTiles(tiles, base)

    os.remove(outfile)
    shutil.rmtree(base)

    assert hits == 2


def test_create_with_byteio():
    """Test loading with a BytesIO boundary"""
    hits = 0
    with open(boundary, "rb") as f:
        boundary_bytes = io.BytesIO(f.read())
    basemap = BaseMapper(boundary_bytes, base, "topo", False)
    tiles = list()
    for level in [8, 9, 10, 11, 12]:
        basemap.getTiles(level)
        tiles += basemap.tiles

    if len(tiles) == 5:
        hits += 1

    if tiles[0].x == 52 and tiles[1].y == 193 and tiles[2].x == 211:
        hits += 1

    outf = DataFile(outfile, basemap.getFormat())
    outf.writeTiles(tiles, base)

    os.remove(outfile)
    shutil.rmtree(base)

    assert hits == 2    
    
    
def test_create_with_bbox():
    """Test loading with a BBOX string"""
    hits = 0
    basemap = BaseMapper(boundary_bbox, base, "topo", False)
    tiles = list()
    for level in [8, 9, 10, 11, 12]:
        basemap.getTiles(level)
        tiles += basemap.tiles

    if len(tiles) == 5:
        hits += 1

    if tiles[0].x == 52 and tiles[1].y == 193 and tiles[2].x == 211:
        hits += 1

    outf = DataFile(outfile, basemap.getFormat())
    outf.writeTiles(tiles, base)

    os.remove(outfile)
    shutil.rmtree(base)

    assert hits == 2    


def test_create_with_invalid_boundary():
    """Test loading with invalid boundary types"""
    hits = 0
    invalid_boundary = 12345  # Invalid boundary type
    try:
        _ = BaseMapper(invalid_boundary, base, "topo", False)
    except ValueError:
        hits += 1

    assert hits == 1
        

if __name__ == "__main__":
    test_create_with_geojson()
    test_create_with_byteio()
    test_create_with_bbox()
    test_create_with_invalid_boundary()
