# -*- coding: utf-8 -*-
"""
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):
    """ Load NeuralNetworkPlugin class.
    :param QgsInterface iface: A QGIS interface instance.
    """

    # MAKE SURE ALL REQUIREMENTS ARE FULFILLED
    try:
        import matplotlib
    except ImportError:
        raise ImportError("Python package 'matplotlib' not found. Please install and restart QGIS. "
                          "For help, see 'https://mlp-image-classifier.readthedocs.io/'.")

    try:
        import sklearn
    except ImportError:
        raise ImportError("Python package 'sklearn' not found. Please install and restart QGIS. "
                          "For help, see 'https://mlp-image-classifier.readthedocs.io/'.")

    try:
        import pyqtgraph
    except ImportError:
        raise ImportError("Python package 'pyqtgraph' not found. Please install and restart QGIS. "
                          "For help, see 'https://mlp-image-classifier.readthedocs.io/'.")

    from lnns.lnns_plugin import NeuralNetworkPlugin
    return NeuralNetworkPlugin(iface)
