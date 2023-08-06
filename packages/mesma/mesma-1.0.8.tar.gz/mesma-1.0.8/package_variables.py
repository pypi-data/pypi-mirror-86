# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : March 2020
| Copyright           : © 2020 by Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
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
dense_name = 'mesma'  # used for distributing your package on pip or qgis, no spaces
long_name = 'MESMA'  # what users see in the QGIS plugin repository and on the RTD toc
pdf_title = 'MESMA Documentation'  # the front page title on the read the docs PDF version

author = 'Ann Crabbé'  # your name
author_email = 'acrabbe.foss@gmail.com'  # your contact information
author_copyright = '© 2018 - 2020 by Ann Crabbé'  # a copyright, typical "© [start year] - [end year] by [your name]"
short_version = '1.0'  # 2 numbers, update with each new release
long_version = '1.0.8'  # 3 numbers, update with each new release

bitbucket_home = 'https://bitbucket.org/kul-reseco/mesma'
bitbucket_src = 'https://bitbucket.org/kul-reseco/mesma/src'
bitbucket_issues = 'https://bitbucket.org/kul-reseco/mesma/issues'

read_the_docs = 'https://mesma.readthedocs.io'

keywords = ['sma', 'mesma', 'szu', 'remote sensing', 'viper', 'spectral mixture analysis']

qgis_min_version = '3.6'

short_description = 'Processing tools for the MESMA (Multiple Endmember Spectral Mixture Analysis) unmixing algorithm.'
long_description = 'MESMA (Multiple Endmember Spectral Mixture Analysis) is a common unmixing technique in the field' \
                   'of remote sensing. This suite of processing tools allows you to unmix your image with MESMA ' \
                   '(with multi-level fusion, stable zone unmixing, ...) and post-process the MESMA results ' \
                   '(visualisation tool, shade normalisation, soft to hard classification).' \

qgis_metadata_icon = 'images/mesma.png'
qgis_category = 'Raster'
processing_provider = False
