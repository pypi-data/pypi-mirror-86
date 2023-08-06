# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : July 2018
| Copyright           : © 2018 - 2020 by Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Translated from VIPER Tools 2.0 (UC Santa Barbara, VIPER Lab).
|                       Dar Roberts, Kerry Halligan, Philip Dennison, Kenneth Dudley, Ben Somers, Ann Crabbé
|
| This file is part of the MESMA plugin and python package.
|
| This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
| License as published by the Free Software Foundation, either version 3 of the License, or any later version.
|
| This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
| warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
|
| You should have received a copy of the GNU General Public License (COPYING.txt). If not see www.gnu.org/licenses.
| ----------------------------------------------------------------------------------------------------------------------
"""
import numpy as np
from osgeo import gdal
from mesma.interfaces import check_path
from mesma.qps.speclib.core import SpectralLibrary


def import_library(path):
    """ Browse for a spectral library and return it as a SpectralLibrary object.

    :param str path: the absolute path to the spectral library
    :return: SpectralLibrary object
    """
    check_path(path)
    spectral_library = SpectralLibrary.readFrom(path)

    if not spectral_library or len(spectral_library) == 0:
        raise Exception("Spectral Library with path {} is empty.".format(path))

    return spectral_library


def import_library_as_array(library: SpectralLibrary) -> np.ndarray:
    """ Return the values of a Spectral Library object.

    :param library: SpectralLibrary object
    :return: numpy array [#good bands x #spectra]
    """
    return np.array([np.array(x.values()['y'])[np.where(x.bbl())[0]] for x in library.profiles()]).T


def import_library_metadata(library: SpectralLibrary, metadata: str) -> np.ndarray:
    """ Return the metadata of a Spectral Library object for a given metadata element.

    :param library: SpectralLibrary object
    :param metadata: the name of the metadata element to return
    :return: string array with metadata [#spectra]
    """

    if metadata not in library.fieldNames():
        raise Exception("{} not found as metadata header; classes found: {}".format(metadata, library.fieldNames()))
    else:
        return np.array([str(x.metadata(metadata)).strip().lower() for x in library.profiles()], dtype=str)


def import_image(path):
    """ Browse for a spectral image and return it without bad bands.
    :param path: the absolute path to the image
    :return: float32 numpy array [#good bands x #rows x #columns]
    """
    check_path(path)

    gdal.UseExceptions()
    try:
        data = gdal.Open(path)
        array = data.ReadAsArray()
        gbl = data.GetMetadataItem('bbl', 'ENVI')
        if gbl is not None:
            gbl = np.asarray(gbl[1:-1].split(","), dtype=int)
            gbl = np.where(gbl == 1)[0]
            array = array[gbl, :, :]
    except Exception as e:
        raise Exception(str(e))

    if array is None or len(array) == 0:
        raise Exception("Image with path {} is empty.".format(path))

    return array


def import_band_names(path):
    """ Browse for the spectral image's band names and return them as a list.
    :param path: the absolute path to the spectral library
    :return: string list of band names
    """
    check_path(path)

    gdal.UseExceptions()
    try:
        data = gdal.Open(path)
        band_names = data.GetMetadataItem('band_names', 'ENVI')
        if band_names:
            band_names = band_names[1:-1].split(",")
            band_names = [x.strip().lower() for x in band_names]
        else:
            raise Exception("The image has no band names. This is not a MESMA Fractions image.")

    except Exception as e:
        raise Exception(e)

    try:
        shade_band_index = band_names.index("shade_fraction")
    except ValueError:
        shade_band_index = None

    return band_names, shade_band_index


def detect_reflectance_scale_factor(array):
    """ Determine the reflectance scale factor [1, 1000 or 10 000] by looking for the largest value in the array.
    :param array: the array for which the reflectance scale factor is to be found
    :return: the reflectance scale factor [int]
    """
    limit = np.nanmax(array)
    if limit < 1:
        return 1
    if limit < 1000:
        return 1000
    if limit < 10000:
        return 10000
    else:
        raise ValueError("Image has values larger than 10000. Cannot process.")
