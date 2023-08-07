# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : April 2020
| Copyright           : © 2020 by Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
|
| This file is part of the QGIS Neural Network MLP Classifier plugin and mlp-image-classifier python package.
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
dense_name = 'mlp-image-classifier'  # used for distributing your package on pip or qgis, no spaces
long_name = 'Neural Network MLPClassifier'  # what users see in the QGIS plugin repository and on the RTD toc
pdf_title = 'Neural Network MLPClassifier Documentation'  # the front page title on the read the docs PDF version

author = 'Ann Crabbé'  # your name
author_email = 'acrabbe.foss@gmail.com'  # your contact information
author_copyright = '© 2018 - 2020 by Ann Crabbé'  # a copyright, typical "© [start year] - [end year] by [your name]"
short_version = '1.0'  # 2 numbers, update with each new release
long_version = '1.0.7'  # 3 numbers, update with each new release

bitbucket_home = 'https://bitbucket.org/kul-reseco/lnns'
bitbucket_src = 'https://bitbucket.org/kul-reseco/lnns/src'
bitbucket_issues = 'https://bitbucket.org/kul-reseco/lnns/issues'

read_the_docs = 'https://mlp-image-classifier.readthedocs.io'

keywords = ['supervised classification', 'neural network', 'remote sensing', 'mlp', 'multi-layer perception classifier',
            'image classification']

qgis_min_version = '3.6'

short_description = 'The Neural Network MLPClassifier predicts classified images using supervised classification.'
long_description = 'Supervised classification of an multi-band image using an MLP (Multi-Layer Perception) Neural ' \
                   'Network Classifier. Based on the Neural Network MLPClassifier by scikit-learn. ' \
                   'Dependencies: pyqtgraph, matplotlib and sklearn. See homepage for clear installation instructions.'

qgis_metadata_icon = 'images/lnns_logo.png'
qgis_category = 'Raster'
processing_provider = True
