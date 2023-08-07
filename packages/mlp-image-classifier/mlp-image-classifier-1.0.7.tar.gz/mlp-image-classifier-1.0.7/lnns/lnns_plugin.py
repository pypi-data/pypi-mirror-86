# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : December 2019
| Copyright           : © 2019 - 2020 by Tinne Cahy (Geo Solutions) and Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Translated from LNNS 1.0 A neural network simulator [C++ software]
|                       Ghent University, Laboratory of Forest Management and Spatial Information Techniques
|                       Lieven P.C. Verbeke
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
from os import path

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu
from qgis.core import QgsApplication

from lnns.interfaces.lnns_gui import NeuralNetworkWidget
from lnns.interfaces.lnns_provider import NeuralNetworkProvider
from lnns.images.lnns_resources_rc import qInitResources
qInitResources()


class NeuralNetworkPlugin:
    """ QGIS Plugin Implementation """

    def __init__(self, iface):
        """
        :param QgsInterface iface: the interface instance which provides the hook to manipulate the QGIS GUI at run time
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = path.dirname(__file__)

        # Add an empty menu to the Raster Menu
        self.main_menu = QMenu(title='Neural Network', parent=self.iface.rasterMenu())
        self.main_menu.setIcon(QIcon(':/lnns_logo'))
        self.iface.rasterMenu().addMenu(self.main_menu)
        self.provider = None

    def initGui(self):
        """ Create the menu entries and toolbar icons inside the QGIS GUI """

        # actions for raster menu
        action = QAction(QIcon(':/lnns_logo'), 'Neural Network MLPClassifier', self.iface.mainWindow())
        action.triggered.connect(self.run_widget)
        action.setStatusTip('Predict image classes using supervised classification (MLPClassifier).')
        self.main_menu.addAction(action)

        # provider for processing toolbox
        self.provider = NeuralNetworkProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.iface.rasterMenu().removeAction(self.main_menu.menuAction())
        QgsApplication.processingRegistry().removeProvider(self.provider)

    @staticmethod
    def run_widget():
        widget = NeuralNetworkWidget()
        widget.show()
        widget.exec_()
